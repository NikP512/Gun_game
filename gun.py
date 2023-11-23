import math
from random import choice, randint

import pygame


FPS = 60

RED = 0xFF0000
BLUE = 0x0000FF
LIGHT_BLUE = (66, 170, 255)
YELLOW = 0xFFC91F
GREEN = 0x00FF00
DARK_GREEN = (0, 69, 36)
HACKY = (128, 107, 42)
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
BROWN = (150, 75, 0)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

G = 1


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
        self.x += self.vx
        self.y -= self.vy
        self.vy -= G

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        return (self.x - obj.x)**2 + (self.y - obj.y)**2 < (self.r + obj.r)**2


class Gun:
    def __init__(self, screen, x, y, place="left"):
        self.screen = screen
        self.place = place
        self.frozen = [0, 0]
        self.growth_power = 1
        self.power = 10
        self.an = 20 if self.place == "left" else 160
        self.x = x
        self.y = y - 15
        self.r = 15
        self.color = (DARK_GREEN, HACKY) if self.place == "left" else (HACKY, DARK_GREEN)

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
        self.an += c
        if self.an > 160:
            self.an = 160
        if self.an < 20:
            self.an = 20

    def power_up(self):
        self.power += self.growth_power
        if self.power < 10 or self.power > 50:
            self.growth_power = -self.growth_power
    
    def draw(self):
        pygame.draw.polygon(self.screen, self.color[0],
                            [(self.x-5*math.sin(math.radians(self.an)),
                              self.y-5*math.cos(math.radians(self.an))),
                             (self.x-5*math.sin(math.radians(self.an))+(30+self.power//2)*math.cos(math.radians(self.an)),
                              self.y-5*math.cos(math.radians(self.an))-(30+self.power//2)*math.sin(math.radians(self.an))),
                             (self.x+5*math.sin(math.radians(self.an))+(30+self.power//2)*math.cos(math.radians(self.an)),
                              self.y+5*math.cos(math.radians(self.an))-(30+self.power//2)*math.sin(math.radians(self.an))),
                             (self.x+5*math.sin(math.radians(self.an)),
                              self.y+5*math.cos(math.radians(self.an)))])
        pygame.draw.circle(self.screen, self.color[1], (self.x, self.y), self.r)
        pygame.draw.polygon(self.screen, self.color[0], [(self.x-30, self.y), (self.x+30, self.y),
                                                      (self.x+20, self.y+15), (self.x-20, self.y+15)])


class StoppedTarget:
    def __init__(self, screen):
        self.screen = screen
        self.r = randint(10, 30)
        self.left_points = 40 - self.r
        self.right_points = 40 - self.r
        self.x = randint(50, WIDTH - 50)
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
        self.left_points = 70 - self.r
        self.right_points = 70 - self.r
        self.x = randint(50, WIDTH - 50)
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
        if (self.x < self.r and self.vx < 0) or (self.x > WIDTH - self.r and self.vx > 0):
            self.vx = -self.vx
        if (self.y < 50 and self.vy > 0) or (self.y > HEIGHT - 50 - self.r and self.vy < 0):
            self.vy = -self.vy


class RandomTarget:
    def __init__(self, screen):
        self.screen = screen
        self.r = randint(10, 30)
        self.left_points = 50 - self.r
        self.right_points = 50 - self.r
        self.x = randint(50, WIDTH - 50)
        self.y = randint(100, HEIGHT - 100)
        self.vx = randint(-10, 10)
        self.vy = randint(-10, 10)
        self.color = (YELLOW, WHITE, BLACK)

    def draw(self):
        pygame.draw.circle(self.screen, self.color[0], (self.x, self.y), self.r, width=self.r//2)
        pygame.draw.circle(self.screen, self.color[1], (self.x, self.y), self.r-self.r//2)
        pygame.draw.circle(self.screen, self.color[2], (self.x, self.y), 2)

    def move(self):
        self.x += self.vx
        self.y -= self.vy
        self.vx = randint(-10, 10)
        self.vy = randint(-10, 10)
        if (self.x < self.r and self.vx < 0) or (self.x > WIDTH - self.r and self.vx > 0):
            self.vx = -self.vx
        if (self.y < 50 and self.vy > 0) or (self.y > HEIGHT - 50 - self.r and self.vy < 0):
            self.vy = -self.vy


class Bomb:
    def __init__(self, screen):
        self.screen = screen
        self.color = BLACK
        self.x = randint(50, WIDTH - 50)
        self.y = 50
        self.r = 5
        self.vy = 0

    def move(self):
        self.y -= self.vy
        self.vy -= G

    def hittest(self, obj):
        return (self.x - obj.x)**2 + (self.y - obj.y)**2 < (self.r + obj.r)**2

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)


class GameEngine:
    def __init__(self):
        pygame.init()
        self.left_points = 0
        self.right_points = 0
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.cadr = 0
        self.left_gun = Gun(self.screen, 50, HEIGHT-50, "left")
        self.left_events = [False, False, False, False, False]
        self.right_gun = Gun(self.screen, WIDTH - 50, HEIGHT-50, "right")
        self.right_events = [False, False, False, False, False]
        self.target1 = StoppedTarget(self.screen)
        self.target2 = MovedTarget(self.screen)
        self.target3 = RandomTarget(self.screen)
        self.left_balls = []
        self.right_balls = []
        self.bombs = []
        self.font = pygame.font.SysFont('timesnewroman', 20)

    def draw(self):
        self.screen.fill(LIGHT_BLUE)
        pygame.draw.rect(self.screen, BROWN, (0, HEIGHT-50, WIDTH, 50))
        self.target1.draw()
        self.target2.draw()
        self.target3.draw()
        for ball in self.left_balls:
            ball.draw()
        for ball in self.right_balls:
            ball.draw()
        for bomb in self.bombs:
            bomb.draw()
        self.left_gun.draw()
        self.right_gun.draw()
        self.screen.blit(self.font.render("Количество очков:" + str(self.left_points), True, BLACK), (10, 10))
        self.screen.blit(self.font.render("Количество очков:" + str(self.right_points), True, BLACK), (WIDTH//2, 10))
        pygame.display.update()
        self.clock.tick(FPS)

    def left_shoot(self):
        new_ball = Ball(self.screen, self.left_gun.x, self.left_gun.y)
        new_ball.vx = self.left_gun.power * math.cos(self.left_gun.an / 180 * math.pi)
        new_ball.vy = self.left_gun.power * math.sin(self.left_gun.an / 180 * math.pi)
        self.left_balls.append(new_ball)
        self.left_points -= 5
        self.left_gun.power = 10
        self.left_gun.growth_power = 1

    def right_shoot(self):
        new_ball = Ball(self.screen, self.right_gun.x, self.right_gun.y)
        new_ball.vx = self.right_gun.power * math.cos(self.right_gun.an / 180 * math.pi)
        new_ball.vy = self.right_gun.power * math.sin(self.right_gun.an / 180 * math.pi)
        self.right_balls.append(new_ball)
        self.right_points -= 5
        self.right_gun.power = 10
        self.right_gun.growth_power = 1

    def checking_events(self):
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
                    case pygame.K_LEFT:
                        self.right_events[0] = True
                    case pygame.K_RIGHT:
                        self.right_events[1] = True
                    case pygame.K_UP:
                        self.right_events[2] = True
                    case pygame.K_DOWN:
                        self.right_events[3] = True
                    case pygame.K_RETURN:
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
                    case pygame.K_LEFT:
                        self.right_events[0] = False
                    case pygame.K_RIGHT:
                        self.right_events[1] = False
                    case pygame.K_UP:
                        self.right_events[2] = False
                    case pygame.K_DOWN:
                        self.right_events[3] = False
                    case pygame.K_RETURN:
                        self.right_events[4] = False
                        self.right_shoot(),
        if self.left_gun.frozen[0] == 0:
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
        if self.right_gun.frozen[0] == 0:
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

    def generate_bombs(self):
        if self.cadr % 200 == 0:
            self.bombs.append(Bomb(self.screen))

    def update(self):
        self.cadr += 1
        self.generate_bombs()
        if self.left_gun.frozen[0] == 1:
            self.left_gun.frozen[1] += 1
        if self.left_gun.frozen[1] >= 100:
            self.left_gun.frozen[0] = 0
            self.left_gun.frozen[1] = 0
        if self.right_gun.frozen[0] == 1:
            self.right_gun.frozen[1] += 1
        if self.right_gun.frozen[1] >= 100:
            self.right_gun.frozen[0] = 0
            self.right_gun.frozen[1] = 0
        for bomb in self.bombs:
            bomb.move()
            if bomb.hittest(self.left_gun):
                self.left_gun.frozen[0] = 1
            if bomb.hittest(self.right_gun):
                self.left_gun.frozen[0] = 1
            if bomb.y > HEIGHT - 50:
                self.bombs.remove(bomb)
        self.target2.move()
        self.target3.move()
        for ball in self.left_balls:
            ball.move()
            if ball.hittest(self.target1):
                self.left_points += self.target1.left_points
                self.target1 = StoppedTarget(self.screen)
                self.left_balls.remove(ball)
            elif ball.hittest(self.target2):
                self.left_points += self.target2.left_points
                self.target2 = MovedTarget(self.screen)
                self.left_balls.remove(ball)
            elif ball.hittest(self.target3):
                self.left_points += self.target3.left_points
                self.target3 = RandomTarget(self.screen)
                self.left_balls.remove(ball)
            elif ball.hittest(self.right_gun):
                self.right_gun.frozen[0] = 1
                self.left_balls.remove(ball)
            elif (ball.x < 0 and ball.vx < 0) or (ball.x > WIDTH and ball.vx > 0):
                self.left_balls.remove(ball)
            elif ball.y > HEIGHT - 50 and ball.vy < 0:
                self.left_balls.remove(ball)
        for ball in self.right_balls:
            ball.move()
            if ball.hittest(self.target1):
                self.right_points += self.target1.right_points
                self.target1 = StoppedTarget(self.screen)
                self.right_balls.remove(ball)
            elif ball.hittest(self.target2):
                self.right_points += self.target2.right_points
                self.target2 = MovedTarget(self.screen)
                self.right_balls.remove(ball)
            elif ball.hittest(self.target3):
                self.right_points += self.target3.right_points
                self.target3 = RandomTarget(self.screen)
                self.right_balls.remove(ball)
            elif ball.hittest(self.left_gun):
                self.left_gun.frozen[0] = 1
                self.right_balls.remove(ball)
            elif (ball.x < 0 and ball.vx < 0) or (ball.x > WIDTH and ball.vx > 0):
                self.right_balls.remove(ball)
            elif ball.y > HEIGHT - 50 and ball.vy < 0:
                self.right_balls.remove(ball)


engine = GameEngine()
while engine.running:
    engine.draw()
    engine.checking_events()
    engine.update()
pygame.quit()
