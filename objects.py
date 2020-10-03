import pygame
import data.engine as e
import sys

#       TODO: add color distinction between platforms

class Platform:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.collider = pygame.Rect((self.x, self.y, 16, 16))
        self.type = "platform"

    def blit(self, display):
        pygame.draw.rect(display, self.color, self.collider)

    def move(self, x, y):
        self.x -= x
        self.collider = pygame.Rect((self.x, self.y, 16, 16))

class Half_Platform(Platform):
    def __init__(self, x, y, color):
        super().__init__(x,y, color)
        self.collider = pygame.Rect((self.x, self.y, 16, 8))
        self.type = "half platform"

class Spike(Half_Platform):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.type = "spike"

    def collide(self, player):
        if player.obj.rect.colliderect(self.collider):
            return True

def gameover():
    pass