import pygame
import time
import random

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.white = (255, 255, 255)
        self.yellow = (255, 255, 102)
        self.black = (0, 0, 0)
        self.red = (213, 50, 80)
        self.green = (0, 255, 0)
        self.blue = (50, 153, 213)
        self.snake_block = 50
        self.snake_speed = 10
        self.block_count = 12
        self.dis_width = self.snake_block * self.block_count
        self.dis_height = self.snake_block * self.block_count
        self.score = 0

    def our_snake(self, snake_block, snake_list):
        cnt = 0
        for x in snake_list[::-1]:
            cnt += 1
            if cnt == 1:
                pygame.draw.rect(self.dis, self.red, [x[0], x[1], snake_block, snake_block])
            else:
                pygame.draw.rect(self.dis, self.green, [x[0], x[1], snake_block, snake_block])
        self.show_score(self.score)

    def message(self, msg, color):
        font_style = pygame.font.SysFont(None, 50)
        mesg = font_style.render(msg, True, color)
        self.dis.blit(mesg, [self.dis_width / 6, self.dis_height / 3])

    def show_score(self, score):
        score_font = pygame.font.SysFont(None, 35)
        score_text = score_font.render("Score: " + str(score), True, self.white)
        self.dis.blit(score_text, [10, 10])

    def game_loop(self):
        game_over = False
        game_close = False

        x1 = self.block_count // 2 * self.snake_block
        y1 = self.block_count // 2 * self.snake_block

        x1_change = 0
        y1_change = 0

        snake_List = []
        Length_of_snake = 1

        foodx = round(random.randrange(0, self.dis_width - self.snake_block) / self.snake_block) * self.snake_block
        foody = round(random.randrange(0, self.dis_height - self.snake_block) / self.snake_block) * self.snake_block
        last_event = 0

        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption('Snake Game')
        clock = pygame.time.Clock()

        while not game_over:
            while game_close:
                self.dis.fill(self.blue)
                self.message("You lost! Press Q-Quit or C-Play Again", self.red)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            self.game_loop()

            changed = 0
            for event in pygame.event.get():
                if changed == 1:
                    continue
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and last_event != 2:
                        x1_change = -self.snake_block
                        y1_change = 0
                        last_event = 1
                        changed = 1
                    elif event.key == pygame.K_RIGHT and last_event != 1:
                        x1_change = self.snake_block
                        y1_change = 0
                        last_event = 2
                        changed = 1
                    elif event.key == pygame.K_UP and last_event != 4:
                        y1_change = -self.snake_block
                        x1_change = 0
                        last_event = 3
                        changed = 1
                    elif event.key == pygame.K_DOWN and last_event != 3:
                        y1_change = self.snake_block
                        x1_change = 0
                        last_event = 4
                        changed = 1

            if x1 >= self.dis_width or x1 < 0 or y1 >= self.dis_height or y1 < 0:
                game_close = True

            x1 += x1_change
            y1 += y1_change
            self.dis.fill(self.black)
            pygame.draw.rect(self.dis, self.yellow, [foodx, foody, self.snake_block, self.snake_block])
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            self.our_snake(self.snake_block, snake_List)

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                self.score += 100
                while [foodx, foody] in snake_List:
                    foodx = round(random.randrange(0, self.dis_width - self.snake_block) / self.snake_block) * self.snake_block
                    foody = round(random.randrange(0, self.dis_height - self.snake_block) / self.snake_block) * self.snake_block

                Length_of_snake += 1

            clock.tick(self.snake_speed)

        pygame.quit()


# Create an instance of the SnakeGame class

# Start the game loop
