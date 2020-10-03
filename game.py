import pygame
import data.engine as e
import sys

WIN_DIM = (600, 400)

window = pygame.display.set_mode(WIN_DIM)
display = pygame.Surface((WIN_DIM[0] / 2, WIN_DIM[1] / 2))

e.load_animations("data/graphics/")

x = 0
y = 0
player = e.entity(x, y, 13, 13, "player")
left = False
right = False
gravity = 0
air_time = 0

#       setting up map and other stuff
map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

tile_coll = [pygame.Rect((0, 200, 300, 1))]

while True:
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
                if event.key == pygame.K_SPACE:
                    if air_time < 4:
                        gravity = -5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False

    #       moving player
    player_movement = [0, 0]
    if right:
        player_movement[0] += 2
    if left:
        player_movement[0] -= 2

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

    #       TODO: debug run anim
    #       setting player anim
    if player_movement[0] == 0:
        player.set_action('idle')
    if player_movement[0] > 0:
        player.set_flip(True)
        player.set_action('run')
    if player_movement[0] < 0:
        player.set_flip(False)
        player.set_action('run')

    #       blitting
    for a in range(len(map)):
        for b in range(len(map[0])):
            if map[a][b] == 0:
                pygame.draw.rect(display, (255, 0, 0), (16 * b, 16 * a, 16, 16))
            else:
                pygame.draw.rect(display, (0, 0, 255), (16 * b, 16 * a, 16, 16))

    player.display(display, [0, 0])
    window.blit(pygame.transform.scale(display, WIN_DIM), [0, 0])
    pygame.display.update()