import pygame
import data.engine as e
import sys

class Platform:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.collider = pygame.Rect((self.x, self.y, 16, 16))
        self.type = "platform"
        self.img = pygame.image.load(e.animation_folder + self.type +".png")

    def blit(self, display):
        display.blit(self.img, (self.x, self.y))

    def move(self, x, y):
        self.x -= x
        self.collider = pygame.Rect((self.x, self.y, 16, 16))

class Half_Platform(Platform):
    def __init__(self, x, y, color):
        super().__init__(x,y, color)
        self.collider = pygame.Rect((self.x, self.y, 16, 8))
        self.type = "half_platform"
        self.img = pygame.image.load(e.animation_folder + self.type +".png")

class Spike(Half_Platform):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.type = "spike"
        self.img = pygame.image.load(e.animation_folder + self.type + ".png")
        self.img.set_colorkey(e.white)

    def collide(self, player):
        if player.obj.rect.colliderect(self.collider):
            return True

class Key:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collider = pygame.Rect((self.x, self.y, 16, 16))
        self.type = "key"
        self.img = e.entity(x, y, 16, 16, self.type)

    def collide(self, player):
        if player.obj.rect.colliderect(self.collider):
            return True

    def blit(self, display):
        self.img.display(display, [0, 0])
        self.img.change_frame(1)

def gameover():
    pass

