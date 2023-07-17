import torch
import random
import numpy as np
from collections import deque
from snake2 import SnakeGame
from DQN_model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 1000000
BATCH_SIZE = 1000
LR = 0.005


class Agent:

    def __init__(self):
        self.game = SnakeGame(50, 5)
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(5**2+5, 256,128, 1)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        block_count = game.block_count
        snake_block = game.snake_block
        head = game.snake_list[0]
        food = game.food
        state = []
        for i in range (0,game.block_count):
            for j in range (0,game.block_count):
                state.append(game.isSafe(i,j))
        state.append(head[0])
        state.append(head[1])
        state.append(food[0])
        state.append(food[1])
        state.append(game.direction)
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 200 - self.n_games*0.5
        final_move=0
        if random.randint(0, 200) < self.epsilon:
            while(True):
                move = random.randint(0,400)%4
                if (move==3 or move ==1 ) and (state[-1] ==3 or state[-1]==1):
                    continue
                elif (move == 2 or move == 4) and (state[-1] == 2 or state[-1] == 4):
                    continue
                else:
                    break

            final_move=move
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move=move

        return final_move


def train():
    game = SnakeGame(50, 5)
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Reward', reward, 'Record:', record)


            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()
