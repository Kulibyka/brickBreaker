import os
import sys

import pygame

size = width, height = 1200, 720
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 255))
FPS = 60
clock = pygame.time.Clock()
pygame.init()
MOVE = 1

# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as error:
        print('Cannot load image:', name)
        raise SystemExit(error)
    image = image.convert_alpha()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def render_start_screen():
    intro_text = ["  Играть", "Правила"]

    fon = pygame.transform.scale(load_image('fon_main1.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 450
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.y = text_coord
        intro_rect.x = 490
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def start_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if 515 < mouse_pos[0] < 680 and 462 < mouse_pos[1] < 509:
                    return
                elif 492 < mouse_pos[0] < 697 and 521 < mouse_pos[1] < 569:
                    rule_screen()
        render_start_screen()
        pygame.display.flip()
        clock.tick(FPS)


def rule_screen():
    rule_text = ["блаблаблаблабла", "блаблаблаблабла", "блаблаблаблабла",
                 "блаблаблаблабла", "блаблаблаблабла", "блаблаблаблабла"]
    fon = pygame.transform.scale(load_image('fon_rules.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 10
    for line in rule_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.y = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    string_rendered = font.render('На главную', True, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.y = 600
    intro_rect.x = 500
    screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                print(mouse_pos)
                if 501 < mouse_pos[0] < 783 and 603 < mouse_pos[1] < 651:
                    print(1)
                    return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(name):
    fullname = "data/" + name
    # читаем уровень, убирая символы перевода строки
    try:
        with open(fullname, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
            FIELD_SIZE = len(level_map[0]), len(level_map)
    except FileNotFoundError as error:
        print('Cannot load image:', name)
        sys.exit()

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def render(lvl_map):
    pygame.draw.line(screen, pygame.Color('white'), (100, 20), (1100, 20), 2)
    pygame.draw.line(screen, pygame.Color('white'), (1100, 20), (1100, 700), 2)
    pygame.draw.line(screen, pygame.Color('white'), (100, 700), (1100, 700), 2)
    pygame.draw.line(screen, pygame.Color('white'), (100, 20), (100, 700), 2)
    color = ['red', 'green', 'blue']
    for i in range(len(lvl_map)):
        for j in range(len(lvl_map[i])):
            Brick(210 + 60 * j, 100 + 20 * i, color[int(lvl_map[i][j])])


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__(tiles_group, all_sprites)
        self.image = load_image(f'{color}.jpg')
        self.rect = self.image.get_rect().move(x, y)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.image = load_image('platform1.jpg')
        self.rect = self.image.get_rect().move(500, 620)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(tiles_group, all_sprites)
        self.image = load_image('ball.jpg')
        self.rect = self.image.get_rect().move(570, 550)


lvl_map = load_level('lvl_1.txt')
movingBall = False
rd = 25
coord = []
s = []
start_screen()
running = True
new_player = Player()
ball = Ball()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            coord.extend([570, 550])
            s.extend([-6, -6])
            movingBall = True
        if event.type == pygame.MOUSEMOTION:
            if event.pos[0] < 186:
                new_player.rect.x = 102
            elif event.pos[0] > 1014:
                new_player.rect.x = 928
            else:
                new_player.rect.x = event.pos[0] - new_player.rect.width // 2
    if movingBall:
        if coord[0] >= 1098 - rd or coord[0] <= 102:
            s[0] = -s[0]
        if coord[1] >= 698 - rd or coord[1] <= 22:
            s[1] = -s[1]
        coord[0] += s[0]
        coord[1] += s[1]
        ball.rect.x, ball.rect.y = coord

        pygame.display.flip()
        clock.tick(100)

    fon = pygame.transform.scale(load_image('fon_game.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    player_group.draw(screen)
    tiles_group.draw(screen)
    render(lvl_map)
    pygame.display.flip()
    clock.tick(FPS)
