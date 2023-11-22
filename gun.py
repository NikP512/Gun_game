import math
from random import choice, randint

import pygame


FPS = 60

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
DARK_GREEN = (0, 69, 36)
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
BROWN = (150, 75, 0)
LIGHT_ZEFIR = (233, 216, 218)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

G = 0


class Ball:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 5
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """

        self.x += self.vx
        self.y -= self.vy
        self.vy -= G

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
    def __init__(self, screen, x, y):
        self.screen = screen
        self.power = 10
        self.an = 20
        self.x = x
        self.y = y - 15
        self.growth_power = 1
        self.color = DARK_GREEN

    def move(self, c):
        self.x += c
        if self.x > WIDTH//2-50:
            self.x = WIDTH//2-50
        if self.x < 50:
            self.x = 50

    def targetting(self, c):
        """Изменение угла выстрела. Увеличение происходит при нажатии 'w', уменьшение -- при нажатии 's'."""
        self.an += c
        if self.an > 160:
            self.an = 160
        if self.an < 20:
            self.an = 20

    def power_up(self):
        """Выбор скорости выстрела. Происходит при удерживании пробела"""
        self.power += self.growth_power
    
    def draw(self):
        pygame.draw.polygon(self.screen, self.color, [(self.x-30, self.y), (self.x+30, self.y), (self.x+20, self.y+15), (self.x-20, self.y+15)])
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 15)
        pygame.draw.polygon(self.screen, self.color,
                            [(self.x-5*math.sin(math.radians(self.an)),
                              self.y-5*math.cos(math.radians(self.an))),
                             (self.x-5*math.sin(math.radians(self.an))+(20+self.power)*math.cos(math.radians(self.an)),
                              self.y-5*math.cos(math.radians(self.an))-(20+self.power)*math.sin(math.radians(self.an))),
                             (self.x+5*math.sin(math.radians(self.an))+(20+self.power)*math.cos(math.radians(self.an)),
                              self.y+5*math.cos(math.radians(self.an))-(20+self.power)*math.sin(math.radians(self.an))),
                             (self.x+5*math.sin(math.radians(self.an)),
                              self.y+5*math.cos(math.radians(self.an)))])


class Target:
    def __init__(self, screen):
        self.screen = screen
        self.r = randint(10, 30)
        self.points = 50 - self.r
        self.x = randint(100, WIDTH - 100)
        self.y = randint(100, HEIGHT - 100)
        self.color = (RED, WHITE, BLACK)

    def draw(self):
        pygame.draw.circle(self.screen, self.color[0], (self.x, self.y), self.r, width=self.r//2)
        pygame.draw.circle(self.screen, self.color[1], (self.x, self.y), self.r-self.r//2)
        pygame.draw.circle(self.screen, self.color[2], (self.x, self.y), 2)


class GameEngine:
    """Игровой "движок", который следит за состоянием объектов и обновляет их."""
    def __init__(self):
        pygame.init()
        self.points = 0
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.gun = Gun(self.screen, 50, HEIGHT-50)
        self.target = Target(self.screen)
        self.balls = []
        self.fonts = [pygame.font.SysFont('timesnewroman', 30), pygame.font.SysFont('timesnewroman', 20)]

    def draw(self):
        """Метод, описывающий отрисовку объектов"""
        self.screen.fill(LIGHT_ZEFIR)
        pygame.draw.rect(self.screen, BROWN, (0, HEIGHT-50, WIDTH, 50))
        self.target.draw()
        for ball in self.balls:
            ball.draw()
        self.gun.draw()
        self.screen.blit(self.fonts[0].render("Количество очков:" + str(self.points), True, BLACK), (10, 10))
        self.screen.blit(self.fonts[1].render("Количество очков в раунде:" + str(self.target.points), True, BLACK), (10, 50))
        pygame.display.update()
        self.clock.tick(FPS)

    def shoot(self):
        """Метод описывает поведение игры при выстреле: создается новый шар, обновляются атрибуты объекта engine."""
        new_ball = Ball(self.screen, self.gun.x, self.gun.y)
        new_ball.vx = self.gun.power * math.cos(self.gun.an / 180 * math.pi)
        new_ball.vy = self.gun.power * math.sin(self.gun.an / 180 * math.pi)
        engine.balls.append(new_ball)
        self.target.points -= 5
        if self.target.points < 0:
            self.target.points = 0
        self.gun.power = 10
        self.gun.growth_power = 1
        self.gun.color = DARK_GREEN

    def checking_events(self):
        """Метод проверяет события, произошедшие за один кадр и вызывает соответствующие методы своих атрибутов."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                self.shoot()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                self.gun.move(1)
            if keys[pygame.K_a]:
                self.gun.move(-1)
            if keys[pygame.K_w]:
                self.gun.targetting(1)
            if keys[pygame.K_s]:
                self.gun.targetting(-1)
            if keys[pygame.K_SPACE]:
                if self.gun.power < 10 or self.gun.power > 50:
                    self.gun.growth_power = -self.gun.growth_power
                self.gun.power_up()

    def update_balls(self):
        for ball in engine.balls:
            ball.move()
            if ball.hittest(engine.target):
                self.points += self.target.points
                engine.target = Target(engine.screen)
                engine.balls.remove(ball)


engine = GameEngine()
while engine.running:
    engine.draw()
    engine.checking_events()
    engine.update_balls()
pygame.quit()
