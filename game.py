import pygame
import data.engine as e
from objects import *
import sys

WIN_DIM = (608, 416)
DISP_DIM = (WIN_DIM[0] / 2, WIN_DIM[1] / 2)

window = pygame.display.set_mode(WIN_DIM)
display = pygame.Surface(DISP_DIM)
pygame.display.set_caption("ldum dare")

e.load_animations("data/graphics/")
e.load_levels("data/levels/")

x = 0
y = DISP_DIM[1] - 13
player = e.entity(x, y, 13, 13, "player")
player.set_flip(True)
left = False
right = False
gravity = 0
air_time = 0
done = False

platforms = []
#       setting up map and other stuff
map = e.level("1")
tile_coll = [pygame.Rect((-50, DISP_DIM[1], DISP_DIM[0] + 100, 1)), pygame.Rect((-16, DISP_DIM[1] - 16, 16, 16))]

for a in range(0, len(map)):
    for b in range(0, len(map[0])):
        if map[a][b] == 1:
            platform = Platform(b * 16, a * 16, "red")
            platforms.append(platform)
            tile_coll.append(platform.collider)
        if map[a][b] == 2:
            platform = Half_Platform(b * 16, a * 16, "red")
            platforms.append(platform)
            tile_coll.append(platform.collider)
        if map[a][b] == 3:
            platform = Half_Platform(b * 16, a * 16 + 8, "red")
            platforms.append(platform)
            tile_coll.append(platform.collider)

while True:
    display.fill(e.black)

    #       event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_SPACE:
                if air_time < 4:
                    gravity = -6
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False

    #       moving player
        #   x axis
    player_movement = [0, 0]
    if right:
        player_movement[0] += 2
    if left:
        player_movement[0] -= 2

        #   y axis
    player_movement[1] += gravity
    gravity += 0.3
    if gravity > 3:
        gravity = 3

    #       moving and checking for touching the ground
    coll = player.move(player_movement, tile_coll)
    if coll['bottom']:
        air_time = 0
        gravity = 0
    else:
        air_time += 1

    if not done and player.x >=DISP_DIM[0]:
        player.set_pos(0, DISP_DIM[1] - 13)

    #       setting player anim
    if player_movement[0] == 0:
        player.set_action('idle')
    if player_movement[0] > 0:
        player.set_flip(True)
        player.set_action('run')
    if player_movement[0] < 0:
        player.set_flip(False)
        player.set_action('run')
    if gravity > 1:
        player.set_action("falling")

    #       blitting
    for a in platforms:
        a.blit(display)
    player.display(display, [0, 0])
    player.change_frame(1)
    window.blit(pygame.transform.scale(display, WIN_DIM), [0, 0])
    pygame.display.update()