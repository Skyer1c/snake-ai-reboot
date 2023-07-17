import math

import gymnasium
import numpy as np

from snake import SnakeGame
scale = 7

class SnakeEnv(gymnasium.Env):
    def __init__(self,snake_block, block_count, seed=42, limit_step=True):
        super().__init__()
        self.game = SnakeGame(snake_block,block_count,seed=seed)
        self.game.reset(seed)
        self.action_space = gymnasium.spaces.Discrete(4) # 0: UP, 1: LEFT, 2: RIGHT, 3: DOWN
        
        self.observation_space = gymnasium.spaces.Box(
            low=0, high=255,
            shape=(block_count*scale,block_count*scale, 3),
            dtype=np.uint8
        )
        if limit_step:
            self.step_limit = block_count**2 # More than enough steps to get the food.
        else:
            self.step_limit = 1e9 # Basically no limit.
        self.steps = 0
    def reset(self,seed=0):
        self.game.reset(seed)
        self.done = False
        self.reward_step_counter = 0

        obs = self._generate_observation()
        info ={
            "snake_size": self.game.snake_length,
            "snake_list": np.array(self.game.snake_list),
            "food_pos": np.array(self.game.food),
            "score": self.game.score
        }
        return obs, info
    def render(self):
        self.game.render()
    def get_action_mask(self):
        return np.array([[self._check_action_validity(a) for a in range(self.action_space.n)]])
    def _check_action_validity(self,action):
        current_direction = self.game.direction
        x1,y1 = self.game.snake_list[0]
        if action==0 and action==1:
            if current_direction==0 and current_direction==1:
                return False
            elif current_direction ==2:
                x1 -= self.snake_block
            else:
                x1 += self.snake_block
        if action==2 and action==3:
            if current_direction==2 and current_direction==3:
                return False
            elif current_direction ==0:
                y1 -= self.snake_block
            else:
                y1 += self.snake_block
        return not ([x1,y1] in self.game.snake_list or x1 >= self.game.dis_width or x1 < 0 or y1 >= self.game.dis_height or y1 < 0)
    def step(self, action):
        info, self.done = self.game.step(action)
        obs = self._generate_observation()
        self.steps+=1
        if self.steps>self.step_limit:
            self.steps=0
            info["score"]-=10
            self.done = True
        if info["snake_size"]>1:
            if np.linalg.norm(info["snake_size"][0] - info["food_pos"]) < np.linalg.norm(info["snake_size"][1] - info["food_pos"]):
                info["score"]+=20 / info["snake_size"]
            else:
                info["score"]-=20 / info["snake_size"]
        return obs, info["score"], self.done, self.done, info
    
    def _generate_observation(self):
        obs = np.zeros((self.game.block_count, self.game.block_count), dtype=np.uint8)
        list1 = np.array(self.game.snake_list)//self.game.snake_block
        # print(np.linspace(200, 50, len(self.game.snake_list/self.game.snake_block), dtype=np.uint8).shape)
        # Set the snake body to gray with linearly decreasing intensity from head to tail.
        obs[tuple(np.transpose(list1))] = np.linspace(200, 50, len(self.game.snake_list), dtype=np.uint8)
        
        # Stack single layer into 3-channel-image.
        obs = np.stack((obs, obs, obs), axis=-1)
        
        # Set the snake head to green and the tail to blue
        obs[tuple(list1[0])] = [0, 255, 0]
        obs[tuple(list1[-1])] = [255, 0, 0]

        # Set the food to red
        obs[np.array(self.game.food)//self.game.snake_block] = [0, 0, 255]

        # Enlarge the observation to 84x84
        obs = np.repeat(np.repeat(obs, scale, axis=0), scale, axis=1)
        return obs