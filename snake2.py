import pygame
import time
import random
import numpy as np
import sys

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)


class SnakeGame:
    def __init__(self, snake_block=50, block_count=12, seed=0):
        pygame.init()

        self.snake_list = []
        self.snake_block = snake_block
        self.snake_speed = 10
        self.block_count = block_count
        self.dis_width = self.snake_block * self.block_count
        self.dis_height = self.snake_block * self.block_count
        self.snake_length = 0
        self.direction = 0
        self.game_over = False
        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption('Snake Game')
        clock = pygame.time.Clock()

        # snake_list: 蛇身体的数组
        #
        # self.game_close=True
        self.seed_value = seed
        random.seed(seed)
        self.reset(seed)
    def isSafe(self,x1,y1):
        if x1 >= self.dis_width or x1 < 0 or y1 >= self.dis_height or y1 < 0 or [x1, y1] in self.snake_list:
            return False
        return True
    def reset(self, seed=0):
        self.game_over = False
        # self.game_close = False
        x1 = self.block_count // 2 * self.snake_block
        y1 = self.block_count // 2 * self.snake_block
        self.snake_list = []
        self.snake_length = 1
        self.snake_list.append([x1, y1])
        foodx = round(random.randrange(0, self.dis_width - self.snake_block) / self.snake_block) * self.snake_block
        foody = round(random.randrange(0, self.dis_height - self.snake_block) / self.snake_block) * self.snake_block
        while [foodx, foody] in self.snake_list:
            foodx = round(random.randrange(0, self.dis_width - self.snake_block) / self.snake_block) * self.snake_block
            foody = round(random.randrange(0, self.dis_height - self.snake_block) / self.snake_block) * self.snake_block
        self.food = [foodx, foody]
        self.score = 0
        self.reward=0

    def distol(self):
        x1, y1 = self.snake_list[0]
        x1 -= self.snake_block
        cnt = 1
        while (self.isSafe(x1, y1)):
            x1 -= self.snake_block
            cnt += 1
        return cnt-1

    def distol(self):
        x1, y1 = self.snake_list[0]
        x1 -= self.snake_block
        cnt = 1
        while (self.isSafe(x1, y1)):
            x1 -= self.snake_block
            cnt += 1
        return cnt-1
    def distor(self):
        x1, y1 = self.snake_list[0]
        x1 += self.snake_block
        cnt = 1
        while (self.isSafe(x1, y1)):
            x1 += self.snake_block
            cnt += 1
        return cnt-1
    def distou(self):
        x1, y1 = self.snake_list[0]
        y1 -= self.snake_block
        cnt = 1
        while (self.isSafe(x1, y1)):
            y1 -= self.snake_block
            cnt += 1
        return cnt-1
    def distod(self):
        x1, y1 = self.snake_list[0]
        y1 += self.snake_block
        cnt = 1
        while (self.isSafe(x1, y1)):
            y1 += self.snake_block
            cnt += 1
        return cnt-1
    def step(self, action):
        x1, y1 = self.snake_list[0]
        if len(self.snake_list) > self.snake_length:
            del self.snake_list[self.snake_length - 1]
        if action == 0:  # up
            y1 -= self.snake_block
            self.direction = 0
        elif action == 1:  # down
            y1 += self.snake_block
            self.direction = 1
        elif action == 2:  # left
            x1 -= self.snake_block
            self.direction = 2
        elif action == 3:  # right
            x1 += self.snake_block
            self.direction = 3

        if x1 >= self.dis_width or x1 < 0 or y1 >= self.dis_height or y1 < 0 or [x1, y1] in self.snake_list:
            self.reward=-1
            self.game_over = True
        self.snake_list.append([x1,y1])
        if len(self.snake_list) > self.snake_length:
            del self.snake_list[0]
        if x1 == self.food[0] and y1 == self.food[1]:
            self.snake_length+=1
            self.reward =10*self.snake_length
            self.score += 1
            foodx = round(
                random.randrange(0, self.dis_width - self.snake_block) / self.snake_block) * self.snake_block
            foody = round(
                random.randrange(0, self.dis_height - self.snake_block) / self.snake_block) * self.snake_block
            while [foodx, foody] in self.snake_list:
                foodx = round(
                    random.randrange(0, self.dis_width - self.snake_block) / self.snake_block) * self.snake_block
                foody = round(
                    random.randrange(0, self.dis_height - self.snake_block) / self.snake_block) * self.snake_block
            self.food = [foodx, foody]

        clock = pygame.time.Clock()
        clock.tick(self.snake_speed)
        self.dis.fill(black)
        pygame.draw.rect(self.dis, yellow, [self.food[0], self.food[1], self.snake_block, self.snake_block])

        self.our_snake(self.snake_block, self.snake_list)
        pygame.display.update()
        # foodx1=self.food[0]
        # foody1=self.food[1]
        # if x1 == foodx1 and y1 == foody1:
        #     self.score += 1
        #     self.reward=10
        #     self.snake_length += 1
        #     while [foodx, foody] in self.snake_list:
        #         foodx = round(
        #             random.randrange(0, self.dis_width - self.snake_block) / self.snake_block) * self.snake_block
        #         foody = round(
        #             random.randrange(0, self.dis_height - self.snake_block) / self.snake_block) * self.snake_block
        #     self.food = [foodx, foody]
        #     self.snake_length += 1
        return self.reward,self.game_over,self.score

    def render(self):
        pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption('Snake Game')
        pygame.draw.rect(self.dis, yellow, [self.food[0], self.food[1], self.snake_block, self.snake_block])
        self.show_score(self.score)
        cnt=0
        for x in self.snake_list[::-1]:
            cnt += 1
            if cnt == 1:
                pygame.draw.rect(self.dis, red, [x[0], x[1], self.snake_block, self.snake_block])
            else:
                pygame.draw.rect(self.dis, green, [x[0], x[1], self.snake_block, self.snake_block])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def our_snake(self, snake_block, snake_list):
        cnt = 0
        for x in snake_list[::-1]:
            cnt += 1
            if cnt == 1:
                pygame.draw.rect(self.dis, red, [x[0], x[1], snake_block, snake_block])
            else:
                pygame.draw.rect(self.dis, green, [x[0], x[1], snake_block, snake_block])
        self.show_score(self.score)

    def message(self, msg, color):
        font_style = pygame.font.SysFont(None, 50)
        mesg = font_style.render(msg, True, color)
        self.dis.blit(mesg, [self.dis_width / 6, self.dis_height / 3])

    def show_score(self, score):
        score_font = pygame.font.SysFont(None, 35)
        score_text = score_font.render("Score: " + str(score), True, white)
        self.dis.blit(score_text, [10, 10])

    # def game_loop(self):
    #     game_over = False
    #     game_close = False
    #
    #     x1 = self.block_count // 2 * self.snake_block
    #     y1 = self.block_count // 2 * self.snake_block
    #
    #     x1_change = 0
    #     y1_change = 0
    #
    #     snake_List = []
    #     length_of_snake = 1
    #
    #     foodx = round(random.randrange(0, self.dis_width - self.snake_block) / self.snake_block) * self.snake_block
    #     foody = round(random.randrange(0, self.dis_height - self.snake_block) / self.snake_block) * self.snake_block
    #     last_event = 0
    #
    #     self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
    #     pygame.display.set_caption('Snake Game')
    #     clock = pygame.time.Clock()
    #
    #     while not game_over:
    #         while game_close:
    #             self.dis.fill(blue)
    #             self.message("You lost! Press Q-Quit or C-Play Again", red)
    #             pygame.display.update()
    #
    #             for event in pygame.event.get():
    #                 if event.type == pygame.KEYDOWN:
    #                     if event.key == pygame.K_q:
    #                         game_over = True
    #                         game_close = False
    #                     if event.key == pygame.K_c:
    #                         self.game_loop()
    #
    #         changed = 0
    #         for event in pygame.event.get():
    #             if changed == 1:
    #                 continue
    #             if event.type == pygame.QUIT:
    #                 game_over = True
    #             if event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.K_LEFT and last_event != 2:
    #                     x1_change = -self.snake_block
    #                     y1_change = 0
    #                     last_event = 1
    #                     changed = 1
    #                 elif event.key == pygame.K_RIGHT and last_event != 1:
    #                     x1_change = self.snake_block
    #                     y1_change = 0
    #                     last_event = 2
    #                     changed = 1
    #                 elif event.key == pygame.K_UP and last_event != 4:
    #                     y1_change = -self.snake_block
    #                     x1_change = 0
    #                     last_event = 3
    #                     changed = 1
    #                 elif event.key == pygame.K_DOWN and last_event != 3:
    #                     y1_change = self.snake_block
    #                     x1_change = 0
    #                     last_event = 4
    #                     changed = 1
    #
    #         if x1 >= self.dis_width or x1 < 0 or y1 >= self.dis_height or y1 < 0:
    #             game_close = True
    #
    #         x1 += x1_change
    #         y1 += y1_change
    #         self.dis.fill(black)
    #         pygame.draw.rect(self.dis, yellow, [foodx, foody, self.snake_block, self.snake_block])
    #         snake_Head = []
    #         snake_Head.append(x1)
    #         snake_Head.append(y1)
    #         snake_List.append(snake_Head)
    #         if len(snake_List) > Length_of_snake:
    #             del snake_List[0]
    #
    #         for x in snake_List[:-1]:
    #             if x == snake_Head:
    #                 game_close = True
    #
    #         self.our_snake(self.snake_block, snake_List)
    #
    #         pygame.display.update()
    #
    #         if x1 == foodx and y1 == foody:
    #             self.score += 1
    #             while [foodx, foody] in snake_List:
    #                 foodx = round(
    #                     random.randrange(0, self.dis_width - self.snake_block) / self.snake_block) * self.snake_block
    #                 foody = round(
    #                     random.randrange(0, self.dis_height - self.snake_block) / self.snake_block) * self.snake_block
    #
    #             Length_of_snake += 1
    #
    #         clock.tick(self.snake_speed)
    #
    #     pygame.quit()


# Create an instance of the SnakeGame class
# game = SnakeGame(50, 12)
# game.game_loop()

# Start the game loop