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
    def __init__(self, screen, x, y, place="left"):
        self.screen = screen
        self.place = place
        self.power = 10
        self.an = 20 if self.place == "left" else 160
        self.x = x
        self.y = y - 15
        self.growth_power = 1
        self.color = DARK_GREEN if self.place == "left" else RED

    def move(self, c):
        self.x += c
        if self.place == "left":
            if self.x > WIDTH//2-50:
                self.x = WIDTH//2-50
            if self.x < 50:
                self.x = 50
        else:
            if self.x > WIDTH-50:
                self.x = WIDTH-50
            if self.x < WIDTH//2+50:
                self.x = WIDTH//2+50

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
        if self.power < 10 or self.power > 50:
            self.growth_power = -self.growth_power
    
    def draw(self):
        pygame.draw.polygon(self.screen, self.color, [(self.x-30, self.y), (self.x+30, self.y),
                                                      (self.x+20, self.y+15), (self.x-20, self.y+15)])
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 15)
        pygame.draw.polygon(self.screen, self.color,
                            [(self.x-5*math.sin(math.radians(self.an)),
                              self.y-5*math.cos(math.radians(self.an))),
                             (self.x-5*math.sin(math.radians(self.an))+(30+self.power)*math.cos(math.radians(self.an)),
                              self.y-5*math.cos(math.radians(self.an))-(30+self.power)*math.sin(math.radians(self.an))),
                             (self.x+5*math.sin(math.radians(self.an))+(30+self.power)*math.cos(math.radians(self.an)),
                              self.y+5*math.cos(math.radians(self.an))-(30+self.power)*math.sin(math.radians(self.an))),
                             (self.x+5*math.sin(math.radians(self.an)),
                              self.y+5*math.cos(math.radians(self.an)))])


class StoppedTarget:
    def __init__(self, screen):
        self.screen = screen
        self.r = randint(10, 30)
        self.left_points = 50 - self.r
        self.right_points = 50 - self.r
        self.x = randint(100, WIDTH - 100)
        self.y = randint(100, HEIGHT - 100)
        self.color = (RED, WHITE, BLACK)

    def draw(self):
        pygame.draw.circle(self.screen, self.color[0], (self.x, self.y), self.r, width=self.r//2)
        pygame.draw.circle(self.screen, self.color[1], (self.x, self.y), self.r-self.r//2)
        pygame.draw.circle(self.screen, self.color[2], (self.x, self.y), 2)


class MovedTarget:
    def __init__(self, screen):
        self.screen = screen
        self.r = randint(10, 30)
        self.left_points = 50 - self.r
        self.right_points = 50 - self.r
        self.x = randint(100, WIDTH - 100)
        self.y = randint(100, HEIGHT - 100)
        self.vx = randint(-10, 10)
        self.vy = randint(-10, 10)
        self.color = (BLUE, WHITE, BLACK)

    def draw(self):
        pygame.draw.circle(self.screen, self.color[0], (self.x, self.y), self.r, width=self.r//2)
        pygame.draw.circle(self.screen, self.color[1], (self.x, self.y), self.r-self.r//2)
        pygame.draw.circle(self.screen, self.color[2], (self.x, self.y), 2)

    def move(self):
        self.x += self.vx
        self.y -= self.vy
        if (self.x < 100 and self.vx < 0) or (self.x > WIDTH - 100 and self.vx > 0):
            self.vx = -self.vx
        if (self.y < 100 and self.vy > 0) or (self.y > HEIGHT - 100 and self.vy < 0):
            self.vy = -self.vy


class GameEngine:
    """Игровой "движок", который следит за состоянием объектов и обновляет их."""
    def __init__(self):
        pygame.init()
        self.left_points = 0
        self.right_points = 0
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.left_gun = Gun(self.screen, 50, HEIGHT-50, "left")
        self.left_events = [False, False, False, False, False]
        self.right_gun = Gun(self.screen, WIDTH - 50, HEIGHT-50, "right")
        self.right_events = [False, False, False, False, False]
        self.target1 = StoppedTarget(self.screen)
        self.target2 = MovedTarget(self.screen)
        self.left_balls = []
        self.right_balls = []
        self.fonts = [pygame.font.SysFont('timesnewroman', 30), pygame.font.SysFont('timesnewroman', 20)]

    def draw(self):
        """Метод, описывающий отрисовку объектов"""
        self.screen.fill(LIGHT_ZEFIR)
        pygame.draw.rect(self.screen, BROWN, (0, HEIGHT-50, WIDTH, 50))
        self.target1.draw()
        self.target2.draw()
        for ball in self.left_balls:
            ball.draw()
        for ball in self.right_balls:
            ball.draw()
        self.left_gun.draw()
        self.right_gun.draw()
        self.screen.blit(self.fonts[0].render("Количество очков:" + str(self.left_points), True, BLACK), (10, 10))
        self.screen.blit(self.fonts[1].render("Количество очков в раунде:" + str(self.target1.left_points+self.target2.left_points), True, BLACK), (10, 50))
        self.screen.blit(self.fonts[0].render("Количество очков:" + str(self.right_points), True, BLACK), (WIDTH-300, 10))
        self.screen.blit(self.fonts[1].render("Количество очков в раунде:" + str(self.target1.right_points+self.target2.right_points), True, BLACK), (WIDTH-300, 50))
        pygame.display.update()
        self.clock.tick(FPS)

    def left_shoot(self):
        """Метод описывает поведение игры при выстреле: создается новый шар, обновляются атрибуты объекта engine."""
        new_ball = Ball(self.screen, self.left_gun.x, self.left_gun.y)
        new_ball.vx = self.left_gun.power * math.cos(self.left_gun.an / 180 * math.pi)
        new_ball.vy = self.left_gun.power * math.sin(self.left_gun.an / 180 * math.pi)
        engine.left_balls.append(new_ball)
        self.target1.left_points -= 5
        self.target2.left_points -= 5
        if self.target1.left_points < 0:
            self.target1.left_points = 0
        if self.target2.left_points < 0:
            self.target2.left_points = 0
        self.left_gun.power = 10
        self.left_gun.growth_power = 1
        self.left_gun.color = DARK_GREEN

    def right_shoot(self):
        """Метод описывает поведение игры при выстреле: создается новый шар, обновляются атрибуты объекта engine."""
        new_ball = Ball(self.screen, self.right_gun.x, self.right_gun.y)
        new_ball.vx = self.right_gun.power * math.cos(self.right_gun.an / 180 * math.pi)
        new_ball.vy = self.right_gun.power * math.sin(self.right_gun.an / 180 * math.pi)
        engine.right_balls.append(new_ball)
        self.target1.right_points -= 5
        self.target2.right_points -= 5
        if self.target1.right_points < 0:
            self.target1.right_points = 0
        if self.target2.right_points < 0:
            self.target2.right_points = 0
        self.right_gun.power = 10
        self.right_gun.growth_power = 1
        self.right_gun.color = RED

    def checking_events(self):
        """Метод проверяет события, произошедшие за один кадр и вызывает соответствующие методы своих атрибутов."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_a:
                        self.left_events[0] = True
                    case pygame.K_d:
                        self.left_events[1] = True
                    case pygame.K_w:
                        self.left_events[2] = True
                    case pygame.K_s:
                        self.left_events[3] = True
                    case pygame.K_SPACE:
                        self.left_events[4] = True
                    case pygame.K_KP4:
                        self.right_events[0] = True
                    case pygame.K_KP6:
                        self.right_events[1] = True
                    case pygame.K_KP8:
                        self.right_events[2] = True
                    case pygame.K_KP2:
                        self.right_events[3] = True
                    case pygame.K_KP5:
                        self.right_events[4] = True
            if event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_a:
                        self.left_events[0] = False
                    case pygame.K_d:
                        self.left_events[1] = False
                    case pygame.K_w:
                        self.left_events[2] = False
                    case pygame.K_s:
                        self.left_events[3] = False
                    case pygame.K_SPACE:
                        self.left_events[4] = False
                        self.left_shoot()
                    case pygame.K_KP4:
                        self.right_events[0] = False
                    case pygame.K_KP6:
                        self.right_events[1] = False
                    case pygame.K_KP8:
                        self.right_events[2] = False
                    case pygame.K_KP2:
                        self.right_events[3] = False
                    case pygame.K_KP5:
                        self.right_events[4] = False
                        self.right_shoot(),
        if self.left_events[0]:
            self.left_gun.move(-1)
        if self.left_events[1]:
            self.left_gun.move(1)
        if self.left_events[2]:
            self.left_gun.targetting(1)
        if self.left_events[3]:
            self.left_gun.targetting(-1)
        if self.left_events[4]:
            self.left_gun.power_up()
        if self.right_events[0]:
            self.right_gun.move(-1)
        if self.right_events[1]:
            self.right_gun.move(1)
        if self.right_events[2]:
            self.right_gun.targetting(-1)
        if self.right_events[3]:
            self.right_gun.targetting(1)
        if self.right_events[4]:
            self.right_gun.power_up()

    def update(self):
        self.target2.move()
        for ball in engine.left_balls:
            ball.move()
            if ball.hittest(engine.target1):
                self.left_points += self.target1.left_points
                engine.target1 = StoppedTarget(engine.screen)
                engine.left_balls.remove(ball)
            if ball.hittest(engine.target2):
                self.left_points += self.target2.left_points
                engine.target2 = MovedTarget(engine.screen)
                engine.left_balls.remove(ball)
        for ball in engine.right_balls:
            ball.move()
            if ball.hittest(engine.target1):
                self.right_points += self.target1.right_points
                engine.target1 = StoppedTarget(engine.screen)
                engine.right_balls.remove(ball)
            if ball.hittest(engine.target2):
                self.right_points += self.target2.right_points
                engine.target2 = MovedTarget(engine.screen)
                engine.right_balls.remove(ball)


engine = GameEngine()
while engine.running:
    engine.draw()
    engine.checking_events()
    engine.update()
pygame.quit()
