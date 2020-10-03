import pygame
import data.engine as e

#       TODO: add color distinction between platforms

class Platform:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.collider = pygame.Rect((self.x, self.y, 16, 16))

    def blit(self, display):
        pygame.draw.rect(display, e.red, self.collider)

class Half_Platform:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.collider = pygame.Rect((self.x, self.y, 16, 8))

    def blit(self, display):
        pygame.draw.rect(display, e.blue, self.collider)