import pygame
import data.engine as e
import sys
import random

active_color = e.blue

class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collider = pygame.Rect((self.x, self.y, 16, 16))
        self.type = "platform"
        self.img = pygame.image.load(e.animation_folder + self.type +".png")

    def blit(self, display):
        display.blit(self.img, (self.x, self.y))

class Half_Platform(Platform):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.collider = pygame.Rect((self.x, self.y, 16, 8))
        self.type = "half_platform"
        self.img = pygame.image.load(e.animation_folder + self.type +".png")

class Spike(Half_Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
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

class Colored(Platform):
    def __init__(self, x, y, color, type):
        super().__init__(x, y)
        self.color = color
        self.type = type
        self.img = pygame.image.load(e.animation_folder + self.type + ".png")
        self.transparent = pygame.image.load(e.animation_folder + self.type + "_transparent.png")

    def blit(self, display):
        if active_color == self.color:
            display.blit(self.img, (self.x, self.y))
        else:
            display.blit(self.transparent, (self.x, self.y))

class Movable(Half_Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.start = (x, y)
        self.end = (0, 0)
        self.dir = "to_end"
        self.type = "movable"

    def move(self):
        self.collider = pygame.Rect((self.x, self.y, 16, 8))
        if self.dir == "to_end":
            if self.end[0] > self.x:
                self.x += 1
            if self.end[0] < self.x:
                self.x -= 1
            if self.end[0] == self.x:
                self.dir = "to_start"

        if self.dir == "to_start":
            if self.start[0] > self.x:
                self.x += 1
            if self.start[0] < self.x:
                self.x -= 1
            if self.start[0] == self.x:
                self.dir = "to_end"