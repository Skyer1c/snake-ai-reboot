import pygame
import time
import random

# Initialize pygame
pygame.init()

# Define colors using RGB values
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Set the width and height of the game window

# Set the title of the game window
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

snake_block = 50
snake_speed = 10

block_count=12

dis_width = snake_block*block_count
dis_height = snake_block*block_count
dis = pygame.display.set_mode((dis_width, dis_height))
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

score=0
def our_snake(snake_block, snake_list):
    cnt=0
    global score
    for x in snake_list[::-1]:
        cnt+=1
        if cnt==1:
            pygame.draw.rect(dis, red, [x[0], x[1], snake_block, snake_block])
        else:
            pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])
    show_score(score)


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width/6, dis_height/3])

def show_score(score):
    score_text = score_font.render("Score: " + str(score), True, white)
    dis.blit(score_text, [10, 10])

def game_loop():
    global score
    global snake_speed
    game_over = False
    game_close = False

    x1 = block_count//2*snake_block
    y1 = block_count//2*snake_block

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
    last_event=0
    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You lost! \nPress Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        changed=0
        for event in pygame.event.get():
            if changed==1:
                continue
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and last_event!=2:
                    x1_change = -snake_block
                    y1_change = 0
                    last_event=1
                    changed=1
                elif event.key == pygame.K_RIGHT and last_event!=1:
                    x1_change = snake_block
                    y1_change = 0
                    last_event= 2
                    changed=1
                elif event.key == pygame.K_UP and last_event!=4:
                    y1_change = -snake_block
                    x1_change = 0
                    last_event=3
                    changed=1
                elif event.key == pygame.K_DOWN and last_event!=3:
                    y1_change = snake_block
                    x1_change = 0
                    last_event=4
                    changed=1
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(black)
        pygame.draw.rect(dis, yellow, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

            Length_of_snake += 1
            snake_speed += 1
            score+=1
        clock.tick(snake_speed)

    pygame.quit()


# Start the game loop
game_loop()

