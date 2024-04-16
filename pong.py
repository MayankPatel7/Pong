import pygame
import random
from time import sleep

# Display setup
pygame.init()
screen = pygame.display.set_mode((1200, 900))
clock = pygame.time.Clock()
FPS = 60
run = True

# Basic setup
pygame.display.set_caption("Pong")
pygame.display.set_icon(pygame.image.load("icon.png"))
font = pygame.font.SysFont("Ariel", 64)
music = pygame.mixer.Sound("loop.mp3")
explosion = pygame.mixer.Sound("explosion.wav")

# Middle net
def draw_net():
    pygame.draw.line(screen, (100, 100, 100), (600, 0), (600, 900), 2)

# Score Renderer
def score_display():
    player1_display = font.render(str(player1.score), True, "White")
    p1_score_pos = player1_display.get_rect(center = (300, 100))
    player2_display = font.render(str(player2.score), True, "White")
    p2_score_pos = player2_display.get_rect(center = (900, 100))
    screen.blit(player1_display, p1_score_pos)
    screen.blit(player2_display, p2_score_pos)

# Paddle Class
class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, initial_pos):
        super().__init__()
        self.surface = pygame.Surface((20, 160))
        self.surface.fill(color)
        self.rect = self.surface.get_rect(center = initial_pos)
        self.score = 0
    def update(self, up, down):
        keys = pygame.key.get_pressed()
        if keys[up]:
            self.rect.y -= 10
        if keys[down]:
            self.rect.y += 10
    def clamp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 900:
            self.rect.bottom = 900

player1 = Paddle("Red", (22, 450))
player2 = Paddle("Blue", (1178, 450))
playerGroup = pygame.sprite.Group(player1, player2)

# Ball Class
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((24, 24))
        self.surface.set_colorkey("Black")
        self.rect = self.surface.get_rect(center = (600, 450))
        self.velX = random.choice((-7, 7))
        self.velY = random.randint(-10, 10)
    def update(self):
        pygame.draw.circle(self.surface, "White", (12, 12), 12)
        self.rect.x += self.velX
        self.rect.y += self.velY
        if self.rect.top <= 0 or self.rect.bottom >= 900:
            self.velY *= -1
        elif self.rect.right <= 0:
            self.rect.center = (600, 450)
            self.velY = random.randint(-10, 10)
            player1.rect.y = 370
            player2.rect.y = 370
            player2.score += 1
            pygame.mixer.Sound.stop(music)
            pygame.mixer.Sound.play(explosion, 0)
            sleep(1)
        elif self.rect.left >= 1200:
            self.rect.center = (600, 450)
            self.velY = random.randint(-10, 10)
            player1.rect.y = 370
            player2.rect.y = 370
            player1.score += 1
            pygame.mixer.Sound.stop(music)
            pygame.mixer.Sound.play(explosion, 0)
            sleep(1)

        if pygame.sprite.spritecollide(self, playerGroup, False):
            self.velX *= -1

ball = Ball()

# Game Loop
while run:
    pygame.mixer.Sound.play(music, 1)
    screen.fill((50, 50, 50))
    draw_net()
    score_display()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(player1.surface, player1.rect)
    player1.update(pygame.K_w, pygame.K_s)
    player1.clamp()
    screen.blit(player2.surface, player2.rect)
    player2.update(pygame.K_UP, pygame.K_DOWN)
    player2.clamp()

    screen.blit(ball.surface, ball.rect)
    ball.update()

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
exit()
