import random
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
dir_sound = path.join(path.dirname(__file__), 'data')
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
    bar_lenght = 100
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
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 70))
        self.image = boss_image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50
        self.speedy = 5
        self.speedx = 5

    def update(self):
        if self.rect.x >= 50 and self.rect.y == 50:
            self.rect.x += self.speedx
        if self.rect.x == 300:
            self.rect.y += self.speedy
        if self.rect.y == 500:
            self.rect.x -= self.speedx
        if self.rect.x == 50:
            self.rect.y -= self.speedy
        global xx, yy, time
        xx = self.rect.x
        yy = self.rect.y
        time += 1
        if time == 10:
            e = Boss_Eggs()
            all_sprites.add(e)
            enem_2.add(e)
            time = 0


class Boss_Eggs():
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image = g_egg
        self.rect = self.image.get_rect()
        self.rect.x = xx + 50
        self.rect.y = yy + 50
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.ranrange(-100, -40)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > height + 10:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.ranrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((16, 15))
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


player_image = load_image("корабль.png", -1)
enemy_image = load_image("egg.png", -1)
bullet_image = load_image("bullet.jpg", -1)
boss_image = load_image("UFO.png", -1)
g_egg = load_image("g_egg.png", -1)
player = Player()
all_sprites.add(player)
score = 0

for i in range(8):
    e = Enemy()
    all_sprites.add(e)
    enem.add(e)

clock = pygame.time.Clock()
running = True
num_hits = 0
boss_spawn_counter = 0
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

boom = pygame.sprite.spritecollide(player, enem, True, pygame.sprite.collide_circle)
for hit in boom:
    boom_sound.play()
    player.hp -= 2
    if player.hp <= 0:
        running = False
    m = Enemy()
    all_sprites.add(m)
    enem.add(m)

boom2 = pygame.sprite.spritecollide(player, enem_2, True, pygame.sprite.collide_circle)
for hit in boom2:
    boom_sound.play()
    player.hp -= 2
    if player.hp <= 0:
        running = False

bulletsss = pygame.sprite.groupcollide(enem, bullets, True, True)
for hit in bulletsss:
    egg_sound.play()
    score += 5
    e = Enemy()
    all_sprites.add(e)
    enem.add(e)
    boss_spawn_counter += 1

if boss_spawn_counter == 5:
    for elem in enem:
        elem.kill()
    b = Boss()
    all_sprites.add(b)
    boss_sprite.add(b)
    boss_spawn_counter = 0

bulle = pygame.sprite.groupcollide(enem_2, bullets, True, True)
for i in bulle:
    egg_sound.play()

boss_check = pygame.sprite.groupcollide(boss_sprite, bullets, False, True)
for hit in boss_check:
    num_hits += 1
if num_hits == 20:
    for elem in boss_sprite:
        elem.kill()
        score += 300
    for i in range(8):
        e = Enemy()
        all_sprites.add(e)
        enem.add(e)
    num_hits = 0

screen.fill((0, 0, 0))
screen.blit(screen, screen_rect)
all_sprites.draw(screen)
draw_text(screen, str(score), 18, width / 2, 10)
draw_text(screen, str(high_score), 18, width / 4, 10)
draw_hp_bar(screen, 390, 10, player.hp)
pygame.display.flip()
if score > int(high_score):
    high_score = score
    print(str(high_score).strip(), file=q)
else:
    print(str(high_score).strip(), file=q)
q.close()
pygame.quit()
