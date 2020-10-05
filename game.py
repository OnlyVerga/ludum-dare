from data.objects import *

pygame.init()
pygame.font.init()
pygame.mixer.set_num_channels(64)

font = pygame.font.Font("data/fonts/Silver.ttf", 20)
big_font = pygame.font.Font("data/fonts/Silver.ttf", 50)
clock = pygame.time.Clock()
main_theme = pygame.mixer.Sound('data/audio/main_theme.wav')
main_theme.play(-1)

thunder_sound = pygame.mixer.Sound('data/audio/lightning.wav')
#exit_level = pygame.mixer.Sound('data/audio/change_scene.wav')

WIN_DIM = (608, 416)
DISP_DIM = (WIN_DIM[0] / 2, WIN_DIM[1] / 2)

#       setup basic stuff
window = pygame.display.set_mode(WIN_DIM)
display = pygame.Surface(DISP_DIM)
pygame.display.set_caption("ludum dare")
life = pygame.image.load("data/graphics/life.png")
e.load_animations("data/graphics/")
e.load_levels("data/levels/")

#       player / level related stuff
global right, left, gravity, air_time, player, done, lives, current_level, platforms, tile_coll

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
text_color = (255, 0, 0)
#       setting up map and other stuff
map = e.level(current_level)


#       change the level map and collision list
def reset(map):
    global platforms, tile_coll
    platforms = []
    global onB
    count = 0

    for a in range(0, len(map)):
        for b in range(0, len(map[0])):
            if map[a][b] != 0:
                count += 1
            if map[a][b] == "1":
                platform = Platform(b * 16, a * 16)
                platforms.append(platform)
            elif map[a][b] == "2":
                platform = Half_Platform(b * 16, a * 16)
                platforms.append(platform)
            elif map[a][b] == "3":
                platform = Half_Platform(b * 16, a * 16 + 8)
                platforms.append(platform)
            elif map[a][b] == "4":
                platform = Spike(b * 16, a * 16 + 8)
                platforms.append(platform)
            elif map[a][b] == "5":
                platform = Key(b * 16, a * 16)
                platforms.append(platform)
            elif map[a][b] == "6":
                platform = Colored(b * 16, a * 16, e.blue, "blue")
                platforms.append(platform)
            elif map[a][b] == "7":
                platform = Colored(b * 16, a * 16, e.red, "red")
                platforms.append(platform)
            elif map[a][b] == "9":
                platform = Movable(b * 16, a * 16)
                buffer = platform
                platforms.append(platform)
            elif map[a][b] == "A":
                buffer.end = (b * 16, a * 16)
            elif map[a][b] == "B":
                platform = Button(b * 16, a * 16)
                onB = onButton(b * 16, a * 16)
                buffer = platform
                platforms.append(platform)
reset(map)

#       tutorial loop
def tut():
    bg = pygame.image.load("data/graphics/bg_intro.png")
    text1 = font.render("An old wizard found an old and obscure book.", False, e.green)
    text2 = font.render("As he read it he became obsessed about it,", False, e.green)
    text3 = font.render("he became ancious and", False, e.green)
    text4 = font.render("he was afraid that someone", False, e.green)
    text5 = font.render("may steal it. One day he made", False, e.green)
    text6 = font.render("a rare magic from the book.", False, e.green)
    text7 = font.render("He was not able to contain it", False, e.green)
    text8 = font.render("and created a space-time loop.", False, e.green)
    text9 = font.render("Help him to escape by collecting", False, e.green)
    text10 = font.render("the magic book in each level", False, e.green)
    text11 = font.render("Move with WASD, jump with SPACE", False, e.green)
    text12 = font.render("Be careful not to touch the spikes", False, e.green)
    text13 = font.render("Or you will lose a soul fragment", False, e.green)
    text14 = font.render("Press SPACE to return to main menu", False, e.green)
    off = 0
    while True:
        display.fill(e.red)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return 0

        display.blit(bg, [0, 0])
        display.blit(text1, ((DISP_DIM[0] - text1.get_width()) / 2, 0 + off))
        display.blit(text2, ((DISP_DIM[0] - text2.get_width()) / 2, 15 + off))
        display.blit(text3, ((DISP_DIM[0] - text3.get_width()) / 2, 30 + off))
        display.blit(text4, ((DISP_DIM[0] - text4.get_width()) / 2, 45 + off))
        display.blit(text5, ((DISP_DIM[0] - text5.get_width()) / 2, 60 + off))
        display.blit(text6, ((DISP_DIM[0] - text6.get_width()) / 2, 75 + off))
        display.blit(text7, ((DISP_DIM[0] - text7.get_width()) / 2, 90 + off))
        display.blit(text8, ((DISP_DIM[0] - text8.get_width()) / 2, 105 + off))
        display.blit(text9, ((DISP_DIM[0] - text9.get_width()) / 2, 120 + off))
        display.blit(text10, ((DISP_DIM[0] - text10.get_width()) / 2, 135 + off))
        display.blit(text11, ((DISP_DIM[0] - text11.get_width()) / 2, 150 + off))
        display.blit(text12, ((DISP_DIM[0] - text12.get_width()) / 2, 165 + off))
        display.blit(text13, ((DISP_DIM[0] - text13.get_width()) / 2, 180 + off))
        display.blit(text14, ((DISP_DIM[0] - text14.get_width()) / 2, 193 + off))
        window.blit(pygame.transform.scale(display, WIN_DIM), [0, 0])
        pygame.display.update()

#       main menu function and loop
def intro():
    text = big_font.render("GAME NAME", False, text_color)
    intro_text = font.render("Start", False, text_color)
    tut_text = font.render("tutorial", False, text_color)
    butt_coll = pygame.Rect(((DISP_DIM[0] - 100)/ 2, 100, 100, 40))
    tut_coll = pygame.Rect(((DISP_DIM[0] - 100) / 2, 160, 100, 40))
    butt = pygame.image.load("data/graphics/butt.png")
    bg = pygame.image.load("data/graphics/bg_intro.png")
    win = e.entity(23, 100, 1, 1, "window")
    win.set_action("idle")
    count = 0
    while True:
        realpos = [0, 0]
        #       event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            realpos[0] = pos[0] / 2
            realpos[1] = pos[1] / 2

        if butt_coll.collidepoint(realpos):
            return 0
        if tut_coll.collidepoint(realpos):
            tut()

        if count == 0:
            if random.random() <= 0.005:
                thunder_sound.play()
                win.set_action("light")
        if win.action == "light":
            count += 1
        if count == 30:
            count = 0
            win.set_action("idle")

        display.blit(bg, [0,0])
        display.blit(text, (DISP_DIM[0] / 2 - text.get_width() / 2, 40))
        display.blit(butt, [(DISP_DIM[0] - 100)/ 2, 100])
        display.blit(butt, [(DISP_DIM[0] - 100)/ 2, 160])
        display.blit(intro_text, (DISP_DIM[0] / 2 - intro_text.get_width() / 2, 112))
        display.blit(tut_text, (DISP_DIM[0] / 2 - tut_text.get_width() / 2, 172))
        win.display(display, [0, 0])
        win.change_frame(1)

        window.blit(pygame.transform.scale(display, WIN_DIM), [0, 0])
        pygame.display.update()

#       gameover loop
def gameover():
    global right, left, gravity, air_time, player, done, lives, current_level, platforms, tile_coll
    player.set_pos(0, DISP_DIM[1] - 13)
    player.set_flip(True)
    left = False
    right = False
    gravity = 0
    air_time = 0
    done = False
    lives = 10
    current_level = 1
    map = e.level(current_level)
    reset(map)
    text = big_font.render("Game Over", False, text_color)
    intro_text = font.render("Play again", False, text_color)
    tut_text = font.render("Quit", False, text_color)
    butt_coll = pygame.Rect(((DISP_DIM[0] - 100) / 2, 100, 100, 40))
    quit_coll = pygame.Rect(((DISP_DIM[0] - 100) / 2, 160, 100, 40))
    butt = pygame.image.load("data/graphics/butt.png")
    bg = pygame.image.load("data/graphics/bg_intro.png")

    while True:
        display.fill(e.black)
        realpos = [0, 0]
        #       event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            realpos[0] = pos[0] / 2
            realpos[1] = pos[1] / 2
        if butt_coll.collidepoint(realpos):
            return 0
        if quit_coll.collidepoint(realpos):
            pygame.quit()
            sys.exit()

        display.blit(bg, [0, 0])
        display.blit(text, (DISP_DIM[0] / 2 - text.get_width() / 2, 40))
        display.blit(butt, [(DISP_DIM[0] - 100) / 2, 100])
        display.blit(butt, [(DISP_DIM[0] - 100) / 2, 160])
        display.blit(intro_text, (DISP_DIM[0] / 2 - intro_text.get_width() / 2, 112))
        display.blit(tut_text, (DISP_DIM[0] / 2 - tut_text.get_width() / 2, 172))

        window.blit(pygame.transform.scale(display, WIN_DIM), [0, 0])
        pygame.display.update()

#       endgame loop
def end():
    global right, left, gravity, air_time, player, done, lives, current_level, platforms, tile_coll
    player.set_pos(0, DISP_DIM[1] - 13)
    player.set_flip(True)
    left = False
    right = False
    gravity = 0
    air_time = 0
    done = False
    lives = 10
    current_level = 1
    map = e.level(current_level)
    reset(map)
    text = big_font.render("YOU ESCAPED!", False, text_color)
    intro_text = font.render("Play again", False, text_color)
    wip_text = font.render("End still WIP", False, text_color)
    tut_text = font.render("Quit", False, text_color)
    butt_coll = pygame.Rect(((DISP_DIM[0] - 100) / 2, 100, 100, 40))
    quit_coll = pygame.Rect(((DISP_DIM[0] - 100) / 2, 160, 100, 40))
    butt = pygame.image.load("data/graphics/butt.png")
    bg = pygame.image.load("data/graphics/bg_intro.png")

    while True:
        display.fill(e.black)
        realpos = [0, 0]
        #       event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            realpos[0] = pos[0] / 2
            realpos[1] = pos[1] / 2
        if butt_coll.collidepoint(realpos):
            return 0
        if quit_coll.collidepoint(realpos):
            pygame.quit()
            sys.exit()

        display.blit(bg, [0, 0])
        display.blit(text, (DISP_DIM[0] / 2 - text.get_width() / 2, 40))
        display.blit(butt, [(DISP_DIM[0] - 100) / 2, 100])
        display.blit(butt, [(DISP_DIM[0] - 100) / 2, 160])
        display.blit(wip_text, [DISP_DIM[0] - wip_text.get_width(), DISP_DIM[1] - wip_text.get_height()])
        display.blit(intro_text, (DISP_DIM[0] / 2 - intro_text.get_width() / 2, 112))
        display.blit(tut_text, (DISP_DIM[0] / 2 - tut_text.get_width() / 2, 172))

        window.blit(pygame.transform.scale(display, WIN_DIM), [0, 0])
        pygame.display.update()

intro()


active_color = e.blue

#       main loop
while True:
    display.fill(e.black)

    #       event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_LEFT):
                left = True
            if event.key in (pygame.K_d, pygame.K_RIGHT):
                right = True
            if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                if air_time < 4:
                    gravity = -6
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_LEFT):
                left = False
            if event.key in (pygame.K_d, pygame.K_RIGHT):
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

    #       updating colls (moving platforms require this to be done every game cycle)
    tile_coll = [pygame.Rect((0, DISP_DIM[1], DISP_DIM[0], 1)), pygame.Rect((-16, DISP_DIM[1] - 16, 16, 16))]
    for a in platforms:
        if a.type != "key" and a.type != "spike":
            if a.type in ("red", "blue"):
                if a.active:
                    tile_coll.append(a.collider)
            else:
                tile_coll.append(a.collider)

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
    if player.x >= DISP_DIM[0]:
        if not done:
            player.set_pos(0, DISP_DIM[1] - 13)
        if done:
            current_level += 1
            if current_level <= 2:
                map = e.level(current_level)
                done = False
                reset(map)
            else:
                end()
                active_color = e.blue

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
    try:
        if onB.collide(player):
            if active_color == e.red:
                active_color = e.blue
            else:
                active_color = e.red
    except:
        pass
    #       blitting
    for a in platforms:
        if a.type == "key":
            if not done:
                a.blit(display)
            if a.collide(player):
                done = True
        elif a.type in ("blue", "red"):
            a.blit(display, active_color)
        else:
            a.blit(display)
        if a.type == "spike":
            if a.collide(player):
                if lives >= 1:
                    lives -= 1
                    player.set_pos(0, DISP_DIM[1] - 13)
                else:
                    gameover()
                active_color = e.blue

        if a.type == "movable":
            a.move()

    #       blit lives
    for a in range(lives):
        display.blit(life, (13 * a, 0))

    player.display(display, [0, 0])
    player.change_frame(1)

    #       rendering
    text = font.render("level: " + str(current_level), False, text_color)
    display.blit(text, (DISP_DIM[0] - text.get_width(), 0))
    window.blit(pygame.transform.scale(display, WIN_DIM), [0, 0])
    pygame.display.update()
    clock.tick(60)