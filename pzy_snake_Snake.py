import pygame, sys

screen_x = 600
screen_y = 600

class Snake(object):
    def __init__(self):
        self.dirction = pygame.K_RIGHT
        self.body = []
        for x in range(5):
            self.addnode()

    def addnode(self):
        left, top = (0, 0)
        if self.body: 
            left, top = (self.body[0].left, self.body[0].top)
        node = pygame.Rect(left, top, 25, 25)
        if self.dirction == pygame.K_LEFT:
            node.left -= 25
        elif self.dirction == pygame.K_RIGHT:
            node.left += 25
        elif self.dirction == pygame.K_UP:
            node.top -= 25
        elif self.dirction == pygame.K_DOWN:
            node.top += 25
        self.body.insert(0, node)

    def delnode(self):
        self.body.pop()

    def isdead(self):
        if self.body[0].x not in range(screen_x):
            return True
        if self.body[0].y not in range(screen_y):
            return True
        if self.body[0] in self.body[1:]:
            return True
        return False
    
    def move(self):
        self.addnode()
        self.delnode()

    def changedirection(self, curkey):
        LR = [pygame.K_LEFT, pygame.K_RIGHT]
        UD = [pygame.K_UP, pygame.K_DOWN]
        if curkey in LR + UD:
            if (curkey in LR) and (self.dirction in LR):
                return
            if (curkey in UD) and (self.dirction in UD):
                return
            self.dirction = curkey
