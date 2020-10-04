from objects import *

pygame.init()
pygame.font.init()

font = pygame.font.SysFont("Verdana.ttf", 10)
big_font = pygame.font.SysFont("Verdana.ttf", 30)
clock = pygame.time.Clock()

WIN_DIM = (608, 416)
DISP_DIM = (WIN_DIM[0] / 2, WIN_DIM[1] / 2)

#       change the level map and collision list
def reset(map):
    global platforms, tile_coll
    platforms = []
    tile_coll = [pygame.Rect((0, DISP_DIM[1], DISP_DIM[0], 1)),
                 pygame.Rect((-16, DISP_DIM[1] - 16, 16, 16))]

    for a in range(0, len(map)):
        for b in range(0, len(map[0])):
            if map[a][b] == "1":
                platform = Platform(b * 16, a * 16, e.red)
                platforms.append(platform)
                tile_coll.append(platform.collider)
            elif map[a][b] == "2":
                platform = Half_Platform(b * 16, a * 16, e.blue)
                platforms.append(platform)
                tile_coll.append(platform.collider)
            elif map[a][b] == "3":
                platform = Half_Platform(b * 16, a * 16 + 8, e.blue)
                platforms.append(platform)
                tile_coll.append(platform.collider)
            elif map[a][b] == "4":
                platform = Spike(b * 16, a * 16 + 8, e.green)
                platforms.append(platform)
            elif map[a][b] == "5":
                platform = Key(b * 16, a * 16)
                platforms.append(platform)
            elif map[a][b] == "6":
                platform = Colored(b * 16, a * 16, e.blue, "blue")
                platforms.append(platform)
                tile_coll.append(platform.collider)
            elif map[a][b] == "7":
                platform = Colored(b * 16, a * 16, e.red, "red")
                platforms.append(platform)
                tile_coll.append(platform.collider)

def intro():
    text = big_font.render("GAME NAME", False, e.green)
    intro_text = font.render("Start", False, e.green)
    tut_text = font.render("tutorial", False, e.green)
    butt = pygame.Rect(((DISP_DIM[0] - 100)/ 2, 100, 100, 40))
    tut = pygame.Rect(((DISP_DIM[0] - 100) / 2, 160, 100, 40))
    while True:
        display.fill(e.black)
        realpos = [0, 0]
        #       event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                realpos[0] = pos[0] / 2
                realpos[1] = pos[1] / 2
        if butt.collidepoint(realpos):
            return 0
        if tut.collidepoint(realpos):
            return 0

        display.blit(text, (DISP_DIM[0] / 2 - text.get_width() / 2, 40))
        pygame.draw.rect(display, e.red, butt)
        pygame.draw.rect(display, e.red, tut)
        display.blit(intro_text, (DISP_DIM[0] / 2 - intro_text.get_width() / 2, 120))
        display.blit(tut_text, (DISP_DIM[0] / 2 - tut_text.get_width() / 2, 180))

        window.blit(pygame.transform.scale(display, WIN_DIM), [0, 0])
        pygame.display.update()


#       setup basic stuff
window = pygame.display.set_mode(WIN_DIM)
display = pygame.Surface(DISP_DIM)
pygame.display.set_caption("ludum dare")
life = pygame.image.load("data/graphics/life.png")

e.load_animations("data/graphics/")
e.load_levels("data/levels/")

#       player / level related stuff
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
global platforms, tile_coll
map = e.level(current_level)
reset(map)

intro()

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

    #       moving and checking for touching the ground or roof
    coll = player.move(player_movement, tile_coll)
    if coll['bottom']:
        air_time = 0
        gravity = 0
    else:
        air_time += 1

    if coll["top"]:
        gravity = 0

    #       stuck in a loop implementation
    if player.x >=DISP_DIM[0]:
        if not done:
            player.set_pos(0, DISP_DIM[1] - 13)
        if done:
            current_level += 1
            map = e.level(current_level)
            done = False
            reset(map)

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


    #       blit lives
    for a in range(lives):
        display.blit(life, (13 * a, 0))

    player.display(display, [0, 0])
    player.change_frame(1)

    #       rendering
    text = font.render("level: " + str(current_level), False, e.black)
    display.blit(text, (DISP_DIM[0] - text.get_width(),0))
    window.blit(pygame.transform.scale(display, WIN_DIM), [0, 0])
    pygame.display.update()
    clock.tick(60)