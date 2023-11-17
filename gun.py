import math
from random import choice, randint

import pygame


FPS = 60

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
LIGHT_ZEFIR = (233, 216, 218)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

G = 1


class Ball:
    def __init__(self, screen, x=0, y=500):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 300

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """

        self.x += self.vx
        self.y -= self.vy
        self.vy -= G
        if self.y >= HEIGHT - self.r and self.vy < 0:
            self.vy = -self.vy//2
        if self.x >= WIDTH - self.r and self.vx > 0 or self.x <= self.r and self.vx < 0:
            self.vx = -self.vx//2


    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        return (self.x - obj.x)**2 + (self.y - obj.y)**2 < (self.r + obj.r)**2

class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.power = 10
        self.an = 0
        self.growth_power = 1
        self.color = GREY

    def get_on(self, keys):
        self.color = RED
        if keys[pygame.K_SPACE]:
            if self.power < 10 or self.power > 50:
                self.growth_power = -self.growth_power
            self.power_up()
        if keys[pygame.K_w]:
            self.targetting(1)
        if keys[pygame.K_s]:
            self.targetting(-1)

    def targetting(self, c):
        """Изменение угла выстрела. Увеличение происходит при нажатии 'w', уменьшение -- при нажатии 's'."""
        self.an += c
        if self.an > 90:
            self.an = 90
        if self.an < 0:
            self.an = 0

    def power_up(self):
        """Выбор скорости выстрела. Происходит при удерживании пробела"""
        self.power += self.growth_power

    def get_off(self, event):
        if event.key == pygame.K_SPACE:
            global bullet
            bullet += 1
            new_ball = Ball(self.screen)
            new_ball.vx = self.power * math.cos(self.an/180*math.pi)
            new_ball.vy = - self.power * math.sin(self.an/180*math.pi)
            engine.balls.append(new_ball)
    
    def draw(self):
        pygame.draw.rect(self.screen, self.color, (0, 500, self.power, 10))

class Target:
    def __init__(self, screen):
        self.screen = screen
        self.points = 0
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.live = 1
        self.r = randint(10, 20)
        self.x = randint(WIDTH//2, WIDTH-self.r)
        self.y = randint(self.r, 500)
        self.color = (RED, WHITE, BLACK)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(self.screen, self.color[0], (self.x, self.y), self.r, width=self.r//2)
        pygame.draw.circle(self.screen, self.color[1], (self.x, self.y), self.r-self.r//2)
        pygame.draw.circle(self.screen, self.color[2], (self.x, self.y), 2)

class Game_Engine:
    """Игровой "движок", который следит за состоянием объектов и обновляет их."""
    def __init__(self, screen):
        self.screen = screen
        self.gun = Gun(screen)
        self.target = Target(screen)
        self.balls = []
    def update(self):
        screen.fill(LIGHT_ZEFIR)
        self.gun.draw()
        self.target.draw()
        for ball in self.balls:
            ball.draw()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0

clock = pygame.time.Clock()
engine = Game_Engine(screen)
finished = False

while not finished:
    engine.update()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            finished = True
        if event.type == pygame.KEYUP:
            engine.gun.get_off(event)
        keys = pygame.key.get_pressed()
        engine.gun.get_on(keys)

    for b in engine.balls:
        b.move()
        if b.hittest(engine.target) and engine.target.live:
            engine.target.live = 0
            b.live = 0
            engine.target.hit()
            engine.target.new_target()
pygame.quit()