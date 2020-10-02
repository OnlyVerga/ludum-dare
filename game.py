import pygame
import data.engine as e
import sys

WIN_DIM = (600, 400)

window = pygame.display.set_mode(WIN_DIM)
display = pygame.Surface((WIN_DIM[0] / 2, WIN_DIM[1] / 2))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()