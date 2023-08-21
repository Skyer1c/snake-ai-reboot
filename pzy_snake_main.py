import sys
import random
import pygame
from Snake import *
from food import *
from game import *
from pygame.locals import *
from data import *

def show_text(screen, pos, text, color, font_bold = False, font_size = 60, font_italic = False):
    cur_font = pygame.font.SysFont("宋体", font_size)
    cur_font.set_bold(font_bold)
    cur_font.set_italic(font_italic)
    text_fmt = cur_font.render(text, 1, color)
    screen.blit(text_fmt, pos)

pygame.init()

game = Game(screen)

while game.running:
    game.new()
    game.run()

pygame.quit()
