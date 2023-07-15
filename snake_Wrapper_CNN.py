import math

import gym
import numpy as np

from snake import SnakeGame
class SnakeEnv(gym.Env):
    def __init__(self,snake_block, block_count, limit_step=True):
        self.game = SnakeGame(snake_block,block_count)
        self.game.reset()
        self.action_space = gym.spaces.Discrete(4) # 0: UP, 1: LEFT, 2: RIGHT, 3: DOWN
        
        self.observation_space = gym.spaces.Box(
            low=0, high=255,
            shape=(block_count,block_count, 3),
            dtype=np.uint8
        )
        if limit_step:
            self.step_limit = block_count**2 # More than enough steps to get the food.
        else:
            self.step_limit = 1e9 # Basically no limit.
        self.reward_step_counter = 0
    def reset(self):
        self.game.reset()
        self.done = False
        self.reward_step_counter = 0

        obs = self._generate_observation()
        return obs
    def render(self):
        self.game.render()
    def generate_observation(self):
        obs = np.zeros((self.game.block_count, self.game.block_count), dtype=np.uint8)

        # Set the snake body to gray with linearly decreasing intensity from head to tail.
        obs[tuple(np.transpose(self.game.snake_list))] = np.linspace(200, 50, len(self.game.snake_list), dtype=np.uint8)
        
        # Stack single layer into 3-channel-image.
        obs = np.stack((obs, obs, obs), axis=-1)
        
        # Set the snake head to green and the tail to blue
        obs[tuple(self.game.snake_list[0])] = [0, 255, 0]
        obs[tuple(self.game.snake_list[-1])] = [255, 0, 0]

        # Set the food to red
        obs[self.game.food] = [0, 0, 255]

        # Enlarge the observation to 84x84

        return obs