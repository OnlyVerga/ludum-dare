from objects import *

clock = pygame.time.Clock()

def reset(map):
    global platforms
    global tile_coll
    platforms = []
    tile_coll = [pygame.Rect((-50, DISP_DIM[1], DISP_DIM[0] + 100, 1)),
                 pygame.Rect((-16, DISP_DIM[1] - 16, 16, 16))]

    for a in range(0, len(map)):
        for b in range(0, len(map[0])):
            if map[a][b] == "1":
                platform = Platform(b * 16, a * 16, e.red)
                platforms.append(platform)
                tile_coll.append(platform.collider)
            if map[a][b] == "2":
                platform = Half_Platform(b * 16, a * 16, e.blue)
                platforms.append(platform)
                tile_coll.append(platform.collider)
            if map[a][b] == "3":
                platform = Half_Platform(b * 16, a * 16 + 8, e.blue)
                platforms.append(platform)
                tile_coll.append(platform.collider)
            if map[a][b] == "4":
                platform = Spike(b * 16, a * 16 + 8, e.green)
                platforms.append(platform)
            if map[a][b] == "5":
                platform = Key(b * 16, a * 16)
                platforms.append(platform)

WIN_DIM = (608, 416)
DISP_DIM = (WIN_DIM[0] / 2, WIN_DIM[1] / 2)

window = pygame.display.set_mode(WIN_DIM)
display = pygame.Surface(DISP_DIM)
pygame.display.set_caption("ludum dare")
life = pygame.image.load("data/graphics/life.png")

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
lives = 10
current_level = 1

#       setting up map and other stuff
global platforms
platforms = []

map = e.level(current_level)
global tile_coll
tile_coll = [pygame.Rect((-50, DISP_DIM[1], DISP_DIM[0] + 100, 1)), pygame.Rect((-16, DISP_DIM[1] - 16, 16, 16))]
reset(map)

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

    if coll["top"]:
        gravity = 0

    if player.x >=DISP_DIM[0]:
        if not done:
            player.set_pos(0, DISP_DIM[1] - 13)
        if done:
            current_level += 1
            map = e.level(current_level)
            reset(map)
            done = False

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

    for a in platforms:
        if a.type == "key":
            if not done:
                a.blit(display)
            if a.collide(player):
                done = True
        else:
            a.blit(display)
        if a.type == "spike":
            if a.collide(player):
                if lives >= 1:
                    lives -= 1
                    player.set_pos(0, DISP_DIM[1] - 13)
                else:
                    gameover()

    for a in range(lives):
        display.blit(life, (13 * a, 0))

    clock.tick(60)
    player.display(display, [0, 0])
    player.change_frame(1)
    window.blit(pygame.transform.scale(display, WIN_DIM), [0, 0])
    pygame.display.update()