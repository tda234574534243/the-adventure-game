import pygame

from world import World, load_level
from player import Player
from enemies import Ghost
from particles import Trail
from projectiles import Bullet, Grenade
from button import Button
from texts import Text, Message, BlinkingText, MessageBox

pygame.init()

# --- WINDOW UPSCALE CONFIG ---------------------------------------------------

GAME_WIDTH, GAME_HEIGHT = 640, 384         # độ phân giải gốc của game
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 768    # độ phân giải hiển thị lên màn hình

# window thật (hiển thị)
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# surface game nội bộ (vẽ mọi thứ lên đây)
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
TILE_SIZE = 16

# scale factors để chuyển mouse coords
SCALE_X = WINDOW_WIDTH / GAME_WIDTH
SCALE_Y = WINDOW_HEIGHT / GAME_HEIGHT

clock = pygame.time.Clock()
FPS = 45

# IMAGES **********************************************************************

BG1 = pygame.transform.scale(pygame.image.load('assets/BG1.png'), (GAME_WIDTH, GAME_HEIGHT))
BG2 = pygame.transform.scale(pygame.image.load('assets/BG2.png'), (GAME_WIDTH, GAME_HEIGHT))
BG3 = pygame.transform.scale(pygame.image.load('assets/BG3.png'), (GAME_WIDTH, GAME_HEIGHT))
MOON = pygame.transform.scale(pygame.image.load('assets/moon.png'), (300, 220))

# FONTS ***********************************************************************

title_font = "Fonts/Aladin-Regular.ttf"
instructions_font = 'Fonts/BubblegumSans-Regular.ttf'

ghostbusters = Message(GAME_WIDTH//2 + 50, GAME_HEIGHT//2 - 90, 90, "GhostBusters", title_font, (255, 255, 255), game_surface)
left_key = Message(GAME_WIDTH//2 + 10, GAME_HEIGHT//2 - 90, 20, "Press left arrow key to go left", instructions_font, (255, 255, 255), game_surface)
right_key = Message(GAME_WIDTH//2 + 10, GAME_HEIGHT//2 - 65, 20, "Press right arrow key to go right", instructions_font, (255, 255, 255), game_surface)
up_key = Message(GAME_WIDTH//2 + 10, GAME_HEIGHT//2 - 45, 20, "Press up arrow key to jump", instructions_font, (255, 255, 255), game_surface)
space_key = Message(GAME_WIDTH//2 + 10, GAME_HEIGHT//2 - 25, 20, "Press space key to shoot", instructions_font, (255, 255, 255), game_surface)
g_key = Message(GAME_WIDTH//2 + 10, GAME_HEIGHT//2 - 5, 20, "Press g key to throw grenade", instructions_font, (255, 255, 255), game_surface)
game_won_msg = Message(GAME_WIDTH//2 + 10, GAME_HEIGHT//2 - 5, 20, "You have won the game", instructions_font, (255, 255, 255), game_surface)

t = Text(instructions_font, 18)
font_color = (12, 12, 12)
play = t.render('Play', font_color)
about = t.render('About', font_color)
controls = t.render('Controls', font_color)
exit = t.render('Exit', font_color)
main_menu = t.render('Main Menu', font_color)

about_font = pygame.font.SysFont('Times New Roman', 20)
with open('Data/about.txt') as f:
    info = f.read().replace('\n', ' ')

# BUTTONS *********************************************************************

ButtonBG = pygame.image.load('Assets/ButtonBG.png')
bwidth = ButtonBG.get_width()

play_btn = Button(GAME_WIDTH//2 - bwidth//4, GAME_HEIGHT//2, ButtonBG, 0.5, play, 10)
about_btn = Button(GAME_WIDTH//2 - bwidth//4, GAME_HEIGHT//2 + 35, ButtonBG, 0.5, about, 10)
controls_btn = Button(GAME_WIDTH//2 - bwidth//4, GAME_HEIGHT//2 + 70, ButtonBG, 0.5, controls, 10)
exit_btn = Button(GAME_WIDTH//2 - bwidth//4, GAME_HEIGHT//2 + 105, ButtonBG, 0.5, exit, 10)
main_menu_btn = Button(GAME_WIDTH//2 - bwidth//4, GAME_HEIGHT//2 + 130, ButtonBG, 0.5, main_menu, 20)

# GROUPS **********************************************************************

trail_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
diamond_group = pygame.sprite.Group()
potion_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

objects_group = [water_group, diamond_group, potion_group, enemy_group, exit_group]

p_image = pygame.transform.scale(pygame.image.load('Assets/Player/PlayerIdle1.png'), (32,32))
p_rect = p_image.get_rect(center=(470, 200))
p_dy = 1
p_ctr = 1

# LEVEL VARIABLES **************************************************************

ROWS = 24
COLS = 40
SCROLL_THRES = 200
MAX_LEVEL = 3

level = 1
level_length = 0
screen_scroll = 0
bg_scroll = 0
dx = 0

# RESET ***********************************************************************

def reset_level(level):
    trail_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    enemy_group.empty()
    water_group.empty()
    diamond_group.empty()
    potion_group.empty()
    exit_group.empty()

    world_data, level_length = load_level(level)
    w = World(objects_group)
    w.generate_world(world_data, game_surface)

    return world_data, level_length, w

def reset_player():
    p = Player(250, 50)
    moving_left = False
    moving_right = False
    return p, moving_left, moving_right

# Khởi tạo p và trạng thái ban đầu tránh lỗi khi nhấn phím trước khi play
p, moving_left, moving_right = reset_player()
w = None
world_data = None

# MAIN GAME *******************************************************************

main_menu = True
about_page = False
controls_page = False
exit_page = False
game_start = False
game_won = True
running = True

def window_to_game_coords(window_pos):
    """Chuyển toạ độ chuột từ cửa sổ -> toạ độ surface game"""
    wx, wy = window_pos
    gx = wx / SCALE_X
    gy = wy / SCALE_Y
    return (gx, gy)

while running:

    # clear game surface
    game_surface.fill((0,0,0))

    for x in range(5):
        game_surface.blit(BG1, ((x*GAME_WIDTH) - bg_scroll * 0.6, 0))
        game_surface.blit(BG2, ((x*GAME_WIDTH) - bg_scroll * 0.7, 0))
        game_surface.blit(BG3, ((x*GAME_WIDTH) - bg_scroll * 0.8, 0))

    if not game_start:
        game_surface.blit(MOON, (-40, 150))

    # lấy trạng thái chuột (trên window thật), chuyển về tọa độ game
    mouse_pos_window = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    mouse_pos_game = window_to_game_coords(mouse_pos_window)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False

            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_UP:
                if not p.jump:
                    p.jump = True
            if event.key == pygame.K_SPACE:
                x, y = p.rect.center
                direction = p.direction
                bullet = Bullet(x, y, direction, (240, 240, 240), 1, game_surface)
                bullet_group.add(bullet)
                p.attack = True
            if event.key == pygame.K_g:
                if p.grenades:
                    p.grenades -= 1
                    grenade = Grenade(p.rect.centerx, p.rect.centery, p.direction, game_surface)
                    grenade_group.add(grenade)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False

    # ------------------------------------------------------------------------
    # ---------------------------  MAIN MENU  --------------------------------
    # ------------------------------------------------------------------------

    if main_menu:
        ghostbusters.update()
        trail_group.update()
        game_surface.blit(p_image, p_rect)
        p_rect.y += p_dy
        p_ctr += p_dy
        if p_ctr > 15 or p_ctr < -15:
            p_dy *= -1
        t = Trail(p_rect.center, (220, 220, 220), game_surface)
        trail_group.add(t)

        if play_btn.draw(game_surface, mouse_pos_game, mouse_pressed):
            world_data, level_length, w = reset_level(level)
            p, moving_left, moving_right = reset_player()

            game_start = True
            main_menu = False
            game_won = False

        if about_btn.draw(game_surface, mouse_pos_game, mouse_pressed):
            about_page = True
            main_menu = False

        if controls_btn.draw(game_surface, mouse_pos_game, mouse_pressed):
            controls_page = True
            main_menu = False

        if exit_btn.draw(game_surface, mouse_pos_game, mouse_pressed):
            running = False

    elif about_page:
        MessageBox(game_surface, about_font, 'GhostBusters', info)
        if main_menu_btn.draw(game_surface, mouse_pos_game, mouse_pressed):
            about_page = False
            main_menu = True

    elif controls_page:
        left_key.update()
        right_key.update()
        up_key.update()
        space_key.update()
        g_key.update()

        if main_menu_btn.draw(game_surface, mouse_pos_game, mouse_pressed):
            controls_page = False
            main_menu = True

    elif exit_page:
        pass

    elif game_won:
        game_won_msg.update()
        if main_menu_btn.draw(game_surface, mouse_pos_game, mouse_pressed):
            controls_page = False
            main_menu = True
            level = 1

    # ------------------------------------------------------------------------
    # --------------------------  GAME START  --------------------------------
    # ------------------------------------------------------------------------

    elif game_start:
        # ensure world loaded
        if w is None:
            world_data, level_length, w = reset_level(level)

        game_surface.blit(MOON, (-40, -10))
        w.draw_world(game_surface, screen_scroll)

        bullet_group.update(screen_scroll, w)
        grenade_group.update(screen_scroll, p, enemy_group, explosion_group, w)
        explosion_group.update(screen_scroll)
        trail_group.update()
        water_group.update(screen_scroll)
        water_group.draw(game_surface)
        diamond_group.update(screen_scroll)
        diamond_group.draw(game_surface)
        potion_group.update(screen_scroll)
        potion_group.draw(game_surface)
        exit_group.update(screen_scroll)
        exit_group.draw(game_surface)

        enemy_group.update(screen_scroll, bullet_group, p)
        enemy_group.draw(game_surface)

        if p.jump:
            t = Trail(p.rect.center, (220, 220, 220), game_surface)
            trail_group.add(t)

        screen_scroll = 0
        p.update(moving_left, moving_right, w)
        p.draw(game_surface)

        if (p.rect.right >= GAME_WIDTH - SCROLL_THRES and bg_scroll < (level_length*TILE_SIZE) - GAME_WIDTH) \
            or (p.rect.left <= SCROLL_THRES and bg_scroll > abs(dx)):
            dx = p.dx
            p.rect.x -= dx
            screen_scroll = -dx
            bg_scroll -= screen_scroll

        if p.rect.bottom > GAME_HEIGHT:
            p.health = 0

        if pygame.sprite.spritecollide(p, water_group, False):
            p.health = 0
            level = 1

        if pygame.sprite.spritecollide(p, diamond_group, True):
            pass

        if pygame.sprite.spritecollide(p, exit_group, False):
            level += 1
            if level <= MAX_LEVEL:
                health = p.health
                world_data, level_length, w = reset_level(level)
                p, moving_left, moving_right = reset_player()
                p.health = health
                screen_scroll = 0
                bg_scroll = 0
            else:
                game_won = True

        potion = pygame.sprite.spritecollide(p, potion_group, False)
        if potion:
            if p.health < 100:
                potion[0].kill()
                p.health += 15
                p.health = min(p.health, 100)

        for bullet in bullet_group:
            enemy =  pygame.sprite.spritecollide(bullet, enemy_group, False)
            if enemy and bullet.type == 1:
                if not enemy[0].hit:
                    enemy[0].hit = True
                    enemy[0].health -= 50
                bullet.kill()
            if bullet.rect.colliderect(p):
                if bullet.type == 2:
                    if not p.hit:
                        p.hit = True
                        p.health -= 20
                    bullet.kill()

        if p.alive:
            color = (0, 255, 0)
            if p.health <= 40:
                color = (255, 0, 0)
            pygame.draw.rect(game_surface, color, (6, 8, p.health, 20), border_radius=10)
        pygame.draw.rect(game_surface, (255, 255, 255), (6, 8, 100, 20), 2, border_radius=10)

        for i in range(p.grenades):
            pygame.draw.circle(game_surface, (200, 200, 200), (20 + 15*i, 40), 5)
            pygame.draw.circle(game_surface, (255, 50, 50), (20 + 15*i, 40), 4)
            pygame.draw.circle(game_surface, (0, 0, 0), (20 + 15*i, 40), 1)

        if p.health <= 0:
            world_data, level_length, w = reset_level(level)
            p, moving_left, moving_right = reset_player()
            screen_scroll = 0
            bg_scroll = 0
            main_menu = True
            about_page = False
            controls_page = False
            game_start = False

    # --------------------------------------------------------------------
    # SCALE TO WINDOW ----------------------------------------------------
    # --------------------------------------------------------------------

    scaled = pygame.transform.scale(game_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
    win.blit(scaled, (0,0))

    clock.tick(FPS)
    pygame.display.update()

pygame.quit()
