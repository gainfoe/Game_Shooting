import pygame
import random

pygame.init()
width = 600
height = 450
bullet_w = 5
bullet_h = 8
enemy_w = 20
enemy_h = 20
gun_w = 20
gun_h = 20
limited_gun_speed = 15
speed_added_to_enemy_and_bullet = 0.05
speed_added_to_gun = 0.05
pos_y_to_create_new_enemy = 50
surface = pygame.display.set_mode((width, height))

background = pygame.image.load("galaxy.jpg")
shooting_sound = pygame.mixer.Sound("shooting_2.wav")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 255)

fps = 80  # frames per second
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
        self.y += pos_gun[1]
        if self.x < 0:
            self.x = 0
        elif self.x > width - self.w:
            self.x = width - self.w
        if self.y < 0:
            self.y = 0
        elif self.y > height - self.h:
            self.y = height - self.h


class Bullet:
    def __init__(self, x_gun, y_gun, w_gun, h_gun, w, h):
        self.bullet_list = []
        self.x = x_gun + w_gun / 2 - w / 2
        self.y = y_gun - h
        self.w = w
        self.h = h

    def draw(self):
        for bullet in self.bullet_list:
            pygame.draw.rect(surface, WHITE, (bullet[0], bullet[1], self.w, self.h))

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
        self.x = random.randint(0, width - enemy_w)
        self.y = 0
        self.w = w
        self.h = h
        self.enemy_list = [[random.randint(0, width - enemy_w), 0]]

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
        if self.enemy_list == [[]]:
            self.x = random.randint(0, width - enemy_w)
            self.y = 0
            self.enemy_list.append([self.x, self.y])
        if self.y >= pos_y_to_create_new_enemy:
            self.x = random.randint(0, width - enemy_w)
            self.y = 0
            self.enemy_list.append([self.x, self.y])
        else:
            pass


class ScoreBoard:
    def __init__(self, score):
        self.score = score

    def display(self):
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

    def hit(self):
        for bullet in self.bullets.bullet_list:
            for enemy in self.enemies.enemy_list:
                if bullet[0] - enemy_w <= enemy[0] <= bullet[0] + bullet_w\
                        and bullet[1] - enemy_h < enemy[1] <= bullet[1] + bullet_h:
                    self.enemies.enemy_list.remove(enemy)
                    self.bullets.bullet_list.remove(bullet)
                    self.scoreboard.score += 1
                    return True

    def death(self, gun):
        for enemy in self.enemies.enemy_list:
            if enemy[1] > height:
                return True
            elif gun.x - enemy_w <= enemy[0] <= gun.x + gun_w\
                        and enemy[1] + enemy_h > gun.y >= enemy[1] - gun_h:
                    return True
            else:
                return False


def main():
    pygame.init()
    gun = Gun(0, height - 50, gun_w, gun_h)
    bullets = Bullet(gun.x, gun.y, gun.w, gun.h, bullet_w, bullet_h)
    enemies = Enemy(enemy_w, enemy_h)
    scoreboard = ScoreBoard(0)
    game = Game(gun, bullets, enemies, scoreboard)
    pos_bullet = [0, -1]
    pos_enemy = [0, 1]
    gun_speed = 5
    flag = False
    while True:
        pos_gun = [0, 0]
        if game.death(gun):
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

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                pos_gun = [gun_speed, 0]
            elif keys[pygame.K_LEFT]:
                pos_gun = [- gun_speed, 0]
            elif keys[pygame.K_DOWN]:
                pos_gun = [0, gun_speed]
            elif keys[pygame.K_UP]:
                pos_gun = [0, - gun_speed]

        if flag:
            break
        game.update(pos_gun, pos_bullet, pos_enemy)
        if game.hit():
            pos_enemy[1] += speed_added_to_enemy_and_bullet
            pos_bullet[1] -= speed_added_to_enemy_and_bullet
            if gun_speed <= limited_gun_speed:
                gun_speed += speed_added_to_gun
            shooting_sound.play()
        game.draw_arena()

        pygame.display.update()

        fps_clock.tick(fps)

    pygame.quit()

if __name__ == '__main__':
    main()
