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
        """"""
        if event.key == pygame.K_SPACE:
            global bullet
            bullet += 1
            new_ball = Ball(self.screen)
            new_ball.vx = self.power * math.cos(self.an/180*math.pi)
            new_ball.vy = self.power * math.sin(self.an/180*math.pi)
            engine.balls.append(new_ball)
            self.power = 10
            self.growth_power = 1
    
    def draw(self):
        pygame.draw.polygon(self.screen, self.color, [(0, 500), (self.power*math.cos(self.an/180*math.pi),500-self.power*math.sin(self.an/180*math.pi)), (10*math.sin(self.an/180*math.pi)+self.power*math.cos(self.an/180*math.pi), 500+10*math.cos(self.an/180*math.pi)-self.power*math.sin(self.an/180*math.pi)), (10*math.sin(self.an/180*math.pi), 500+10*math.cos(self.an/180*math.pi))])


class Target:
    def __init__(self, screen):
        self.screen = screen
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.live = 1
        self.r = randint(10, 20)
        self.x = randint(WIDTH//2, WIDTH-self.r)
        self.y = randint(self.r, 500)
        self.color = (RED, WHITE, BLACK)

    def draw(self):
        pygame.draw.circle(self.screen, self.color[0], (self.x, self.y), self.r, width=self.r//2)
        pygame.draw.circle(self.screen, self.color[1], (self.x, self.y), self.r-self.r//2)
        pygame.draw.circle(self.screen, self.color[2], (self.x, self.y), 2)


class GameEngine:
    """Игровой "движок", который следит за состоянием объектов и обновляет их."""
    def __init__(self):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.gun = Gun(self.screen)
        self.target = Target(self.screen)
        self.balls = []

    def update(self):
        self.screen.fill(LIGHT_ZEFIR)
        self.gun.draw()
        self.target.draw()
        for ball in self.balls:
            ball.draw()
            ball.move()
        pygame.display.update()
        self.clock.tick(FPS)

    def shoot(self):
        new_ball = Ball(self.screen)
        new_ball.vx = self.gun.power * math.cos(self.gun.an / 180 * math.pi)
        new_ball.vy = self.gun.power * math.sin(self.gun.an / 180 * math.pi)
        engine.balls.append(new_ball)
        self.gun.power = 10
        self.gun.growth_power = 1

    def checking_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                self.shoot()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if self.gun.power < 10 or self.gun.power > 50:
                    self.gun.growth_power = -self.gun.growth_power
                self.gun.power_up()
            if keys[pygame.K_w]:
                self.gun.targetting(1)
            if keys[pygame.K_s]:
                self.gun.targetting(-1)


engine = GameEngine()
while engine.running:
    engine.update()
    engine.checking_events()

    for b in engine.balls:
        if b.hittest(engine.target) and engine.target.live:
            engine.target.live = 0
            b.live = 0
            engine.target.new_target()
pygame.quit()