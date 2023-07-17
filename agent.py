import torch
import random
import numpy as np
from collections import deque
from snake2 import SnakeGame
from DQN_model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.005


class Agent:

    def __init__(self):
        self.game = SnakeGame(50, 5)
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(5, 256,128, 1)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        block_count = game.block_count
        snake_block = game.snake_block
        head = game.snake_list[0]
        food = game.food
        state = [
            game.new_disto(0),
            game.new_disto(1),
            game.new_disto(2),
            game.isfood(0),
            game.isfood(1)
        ]
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
        self.epsilon = 100 - self.n_games*0.5
        final_move=0
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0,3)
            final_move=move
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move=move
        print("final_move=",final_move)
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
        print("fuckfuck1")
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        # print("fuckfuck2")
        reward, done, score = game.new_step(final_move)
        # print("fuckfuck3")
        state_new = agent.get_state(game)
        # print("fuckfuck4")

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        # print("fuckfuck5")
        if done:
            # train long memory, plot result
            # print("fuckfuck6")
            game.reset()
            # print("fuckfuck7")
            agent.n_games += 1
            agent.train_long_memory()
            # print("fuckfuck8")
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
