import pygame
# from pygame.locals import *
import random

pygame.init()
width = 600
height = 500

surface = pygame.display.set_mode((width, height))

background = pygame.image.load("galaxy.jpg")
shooting_sound = pygame.mixer.Sound("shooting_2.wav")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
SKY = (0, 255, 255)
GREEN = (0, 255, 0)

fps = 200  # frames per second
fps_clock = pygame.time.Clock()

class Gun:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    def draw(self):
        pygame.draw.rect(surface, GREEN, (self.x, self.y, self.w, self.h))
    def move(self, pos_gun):
        self.x += pos_gun[0]
        if self.x < 0:
            self.x = 0
        if self.x > width - self.w:
            self.x = width - self.w

class Bullet:
    def __init__(self, x_gun, y_gun, w_gun, h_gun, w, h):
        self.bullet_list = []
        self.x = x_gun + w_gun / 2 - w / 2
        self.y = y_gun - h
        self.w = w
        self.h = h
    def draw(self):
        for bullet in self.bullet_list:
            pygame.draw.rect(surface, SKY, (bullet[0], bullet[1], self.w, self.h))
    def move(self, pos_bullet):
        for bullet in self.bullet_list:
            bullet[0] += pos_bullet[0]
            bullet[1] += pos_bullet[1]
    def new_bullet(self, gun):
        self.x = gun.x + gun.w / 2 - self.w / 2
        self.y = gun.y - self.h
        self.bullet_list.append([self.x, self.y])

class Enemy:
    def __init__(self, w, h):
        self.x = random.randint(0, 19) * 30
        self.y = 0
        self.w = w
        self.h = h
        self.enemy_list = [[random.randint(0, 18) * 30, 0]]
    def draw(self):
        for enemy in self.enemy_list:
            pygame.draw.rect(surface, RED, (enemy[0], enemy[1], self.w, self.h))
    def move(self, pos_enemy):
        for enemy in self.enemy_list:
            enemy[0] += pos_enemy[0]
            enemy[1] += pos_enemy[1]
        self.y += pos_enemy[1]
        self.x += pos_enemy[0]
    def new_enemy(self):
        if self.enemy_list == []:
            self.x = random.randint(0, 19) * 30
            self.y = 0
            self.enemy_list.append([self.x, self.y])
        if self.y >= 50:
            self.x = random.randint(0, 19) * 30
            self.y = 0
            self.enemy_list.append([self.x, self.y])
        else:
            pass

class ScoreBoard:
    def __init__(self, x, y, score, size):
        self.x = x
        self.y = y
        self.score = score
        self.size = size
        self.font = pygame.font.Font(None, self.size)

    def display(self):
        # display_score = self.font.render("Score: " + str(self.score), True, WHITE)
        # surface.blit(display_score, (self.x, self.y))
        pygame.display.set_caption("Shooting Game. Score: " + str(self.score))


class Game:
    def __init__(self, gun, bullets, enemies, scoreboard):
        self.enemies = enemies
        self.gun = gun
        self.bullets = bullets
        self.scoreboard = scoreboard

    def draw_arena(self):
        surface.blit(background, (0, 0))
        self.gun.draw()
        self.bullets.draw()
        self.enemies.draw()
        self.scoreboard.display()

    def update(self, pos_gun, pos_bullet, pos_enemy):
        self.gun.move(pos_gun)
        self.bullets.move(pos_bullet)
        self.bullets.new_bullet(self.gun)
        self.enemies.new_enemy()
        self.enemies.move(pos_enemy)
        for bullet in self.bullets.bullet_list:
            for enemy in self.enemies.enemy_list:
                if int(bullet[0] + self.bullets.w / 2) == int(enemy[0] + self.enemies.w / 2)\
                        and int(bullet[1]) == int(enemy[1] + self.enemies.h):
                    self.enemies.enemy_list.remove(enemy)
                    self.bullets.bullet_list.remove(bullet)
                    self.scoreboard.score += 1
                    pos_enemy[1] += 0.1
                    shooting_sound.play()

    def death(self):
        for enemy in self.enemies.enemy_list:
            if enemy[1] > height:
                return True
            else:
                return False


def Main():
    pygame.init()
    gun = Gun(0, height - 50, 30, 30)
    bullets = Bullet(gun.x, gun.y, gun.w, gun.h, 10, 10)
    enemies = Enemy(30, 30)
    scoreboard = ScoreBoard(610, 0, 0, 50)
    game = Game(gun, bullets, enemies, scoreboard)
    pos_bullet = [0, -1]
    pos_enemy = [0, 0.1]
    flag = False
    while True:
        pos_gun = [0, 0]
        if game.death():
            surface.blit(background, (0, 0))
            for i in range(500):
                font = pygame.font.Font(None, 100)
                game_over = font.render("Game Over ! ", True, WHITE)
                surface.blit(game_over, (10, height / 4))
                score_display = font.render("Your Score: " + str(game.scoreboard.score), True, WHITE)
                surface.blit(score_display, (10, height / 2))
                pygame.display.update()
            flag = True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    flag = True
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        pos_gun = [30, 0]
                    elif event.key == pygame.K_LEFT:
                        pos_gun = [- 30, 0]

        if flag:
            break
        game.update(pos_gun, pos_bullet, pos_enemy)
        game.draw_arena()

        pygame.display.update()

        fps_clock.tick(fps)

    pygame.quit()

if __name__ == '__main__':
    Main()


