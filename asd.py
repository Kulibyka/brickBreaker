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
LIVES = 3

# основной персонаж
player = None

# группы спрайтов
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bricks_group = pygame.sprite.Group()


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
    rule_text = [" Игрок должен разбить стену из кирпичей,", "отразив прыгающий мяч платформой.",
                 "Платформа управляется мышью компьютера.", "Для начала игрок получает 3 жизни",
                 "Жизнь теряется, если мяч попадает", "в нижнюю часть экрана.",
                 "Если жизни потеряны - игра окончена.", "Цель - уничтожить все кирпичики."]
    fon = pygame.transform.scale(load_image('fon_rules.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 10
    for line in rule_text:
        string_rendered = font.render(line, True, (185, 198, 237))
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


def render():
    pygame.draw.line(screen, pygame.Color('white'), (100, 20), (1100, 20), 2)
    pygame.draw.line(screen, pygame.Color('white'), (1100, 20), (1100, 700), 2)
    pygame.draw.line(screen, pygame.Color('white'), (100, 700), (1100, 700), 2)
    pygame.draw.line(screen, pygame.Color('white'), (100, 20), (100, 700), 2)


def generate_level(lvl_map):
    color = ['red', 'green', 'blue']
    for i in range(len(lvl_map)):
        for j in range(len(lvl_map[i])):
            if lvl_map[i][j] != ' ':
                Brick(210 + 60 * j, 100 + 20 * i, color[int(lvl_map[i][j])])


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__(bricks_group)
        self.image = load_image(f'{color}.jpg')
        self.rect = self.image.get_rect().move(x, y)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group)
        self.image = load_image('platform1.jpg')
        self.rect = self.image.get_rect().move(500, 620)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(tiles_group)
        self.image = load_image('ball1.jpg')
        self.rect = self.image.get_rect().move(570, 550)
        self.movingBall = False
        self.speed = [-10, -10]
        self.coord = [570, 550]

    def delete(self, x, y):
        for sprite in bricks_group:
            if (x, y) == sprite.rect.topleft:
                bricks_group.remove(sprite)
                break

    def move(self):
        self.movingBall = not self.movingBall

    def update(self):
        if self.movingBall:
            if self.coord[1] >= 630:
                # LIVES -= 1
                ball.move()
                self.delete(self.rect[0], self.rect[1])
                self.rect = self.image.get_rect().move(570, 550)
                pass
            if self.coord[0] >= 1098 - rd or self.coord[0] <= 102:
                self.speed[0] = -self.speed[0]
            if self.coord[1] >= 698 - rd or self.coord[1] <= 22:
                self.speed[1] = -self.speed[1]
            if pygame.sprite.spritecollideany(self, bricks_group):
                x, y = pygame.sprite.spritecollideany(self, bricks_group).rect.topleft
                x_b, y_b = self.rect.topleft
                if x_b < x <= x_b + 20 and y <= y_b + 10 <= y + 20:
                    self.speed[0] = -self.speed[0]
                    self.delete(x, y)
                elif y_b < y <= y_b + 20 and x <= x_b + 10 <= x + 60:
                    self.speed[1] = -self.speed[1]
                    self.delete(x, y)
                elif x_b <= x + 60 < x_b + 20 and y <= y_b + 10 <= y + 20:
                    self.speed[0] = -self.speed[0]
                    self.delete(x, y)
                elif y_b <= y + 20 < y_b + 20 and x <= x_b + 10 <= x + 60:
                    self.speed[1] = -self.speed[1]
                    self.delete(x, y)
            if pygame.sprite.spritecollideany(self, player_group):
                x, y = pygame.sprite.spritecollideany(self, player_group).rect.topleft
                x_b, y_b = self.rect.topleft
                if (x_b < x <= x_b + 20 or x_b <= x + 172 < x_b + 20) and y <= y_b + 10 <= y + 32:
                    self.speed[0] = -self.speed[0]
                elif y_b < y <= y_b + 20 and x <= x_b + 10 <= x + 172:
                    if x + 86 <= x_b:
                        k = (x + 172 - x_b) / 86
                        self.speed[0] = int((200 * (1 - k)) ** 0.5)
                        self.speed[1] = -int((200 * k) ** 0.5)
                    else:
                        k = (x_b - x) / 86
                        self.speed[0] = -int((200 * (1 - k)) ** 0.5)
                        self.speed[1] = -int((200 * k) ** 0.5)
                print(self.speed)
            self.coord[0] += self.speed[0]
            self.coord[1] += self.speed[1]

            ball.rect.x, ball.rect.y = self.coord


rd = 20
start_screen()
generate_level(load_level('lvl_1.txt'))
running = True
new_player = Player()
ball = Ball()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            ball.move()
        if event.type == pygame.MOUSEMOTION:
            if event.pos[0] < 186:
                new_player.rect.x = 102
            elif event.pos[0] > 1014:
                new_player.rect.x = 928
            else:
                new_player.rect.x = event.pos[0] - new_player.rect.width // 2
    fon = pygame.transform.scale(load_image('fon_game.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    ball.update()
    player_group.draw(screen)
    tiles_group.draw(screen)
    bricks_group.draw(screen)
    render()
    pygame.display.flip()
    clock.tick(FPS)