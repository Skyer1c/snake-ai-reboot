import sys, pygame
from pygame.locals import *
from Snake import *
from food import *
from data import *

def show_text(screen, pos, text, color, font_bold = False, font_size = 60, font_italic = False):
    cur_font = pygame.font.SysFont("宋体", font_size)
    cur_font.set_bold(font_bold)
    cur_font.set_italic(font_italic)
    text_fmt = cur_font.render(text, 1, color)
    screen.blit(text_fmt, pos)

class Game(pygame.sprite.Sprite):
    def __init__(self, surface) -> None:
        self.surface = surface
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('snake')
        self.running = True
        self.playing = True
    
    def new(self):
        self.scores = 0
        self.isdead = False
        self.playing = True
        self.snake = Snake()
        self.food = Food()
        

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.quit:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                self.snake.changedirection(event.key)
                if event.key == pygame.K_SPACE and self.isdead:
                    self.playing = True
                    return
        self.isdead = self.snake.isdead()
        if self.isdead:
            self.playing = False
            return
        self.snake.move()
        if self.food.rect == self.snake.body[0]:
            self.scores += 50
            self.food.remove()
            self.snake.addnode()
        self.food.set()
        self.clock.tick(FPS)

    def draw(self):
        screen.fill((255, 255, 255))
        for rect in self.snake.body:
            pygame.draw.rect(screen, (20, 220, 39), rect, 0)
        if self.isdead:
            show_text(screen, (100, 200), 'You Dead!', (227, 29, 18), False, 100)
            show_text(screen, (150, 300), 'press space to try again...', (0, 0, 22), False, 30)
        pygame.draw.rect(screen, (136, 0, 24), self.food.rect, 0)
        show_text(screen, (50, 500), 'Scores:' + str(self.scores), (223, 223, 223))
        pygame.display.update()
    
    def run(self):
        
        while self.playing:
            self.update()
            self.draw()
        while self.playing == False:
            self.update()
