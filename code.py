import pygame
import os
import sys
from os import path

pygame.init()
size = width, height = 500, 800
FPS = 60
all_sprites = pygame.sprite.Group()
boss_sprite = pygame.sprite.Group()
b_eggs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enem = pygame.sprite.Group()
enem_2 = pygame.sprite.Group()
screen = pygame.display.set_mode(size)
screen_rect = screen.get_rect()
dir_sound = path.join(path.dirname(__file__), 'sounds')
shoot_sound = pygame.mixer.Sound(path.join(dir_sound, 'pew.wav'))
egg_sound = pygame.mixer.Sound(path.join(dir_sound, 'egg.wav'))
boom_sound = pygame.mixer.Sound(path.join(dir_sound, 'boom.wav'))
xx = 0
yy = 0
p = 0
time = 0
f = open("High_Score.txt", mode="r")
high_score = str(f.read()).strip()
f.close()
q = open("High_Score.txt", mode="w")


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


font_name = pygame.font.match_font('Times New Roman')


def draw_text(surf, text, size, x, y):
    color = (255, 255, 0)
    if text == str(high_score):
        color = (0, 255, 255)
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_hp_bar(surf, x, y, a):
    if a < 0:
        a = 0
    bar_lenght = 100 +
    bar_height = 10
    fill = (a / 10) * bar_lenght
    outline_rect = pygame.Rect(x, y, bar_lenght, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, (255, 255, 0), fill_rect)
    pygame.draw.rect(surf, (0, 0, 255), outline_rect, 2)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite._init__(self)
        self.image = pygame.Surface((45, 46))
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height - 20
        self.speed = 0
        self.hp = 10


def update(self):
    self.speed = 0
    what = pygame.key.get_pressed()
    if what[pygame.K_LEFT]:
        self.speed = -5
    if what[pygame.K_RIGHT]:
        self.speed = 5
    self.rect.x += self.speed
    if self.rect.x >= width - 55:
        self.rect.x = width - 55
    if self.rect.x <= 0:
        self.rect.x = 5


def shoot(self):
    bullet = Bullet(self.rect.centerx, self.rect.top)
    all_sprites.add(bullet)
    bullets.add(bullet)
    shoot_sound.play()


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pass

    def update(self):
        pass


class Enemy(pygame.sprite.Sprite):
        def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIGHT - self.rect.width)
        self.rect.y = random.ranrange(-100, -40)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIGHT - self.rect.width)
            self.rect.y = random.ranrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class bullet(pygame.sprite.Sprite):
    def __init__(self):
        pass

    def update(self):
        pass
