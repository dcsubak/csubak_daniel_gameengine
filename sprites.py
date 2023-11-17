# This file was created by: Daniel Csubak

import pygame as pg
from pygame.sprite import Sprite
from random import randint
from pygame.math import Vector2 as vec
import os
from settings import *

# setup asset folders here - images sounds etc...
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # self.image = pg.Surface((50, 50))...
        # self.image.fill(GREEN)...
        # use an image for player sprite...
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, 'theBigBell.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0) 
        self.can_jump = True

    def controls(self):
        # which each keystroke does what input in the game...
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.x = 5
        # can use w key and spacebar to jump...
        if keys[pg.K_w]:
            self.jump()
        if keys[pg.K_SPACE]:
            self.jump()

    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        self.rect.y -= 1
        if hits and self.can_jump:
            self.vel.y = -PLAYER_JUMP
            self.can_jump = False
              # checking for player is on top of platform...
            if self.vel.y > 0 and (self.rect.bottom - hits[0].rect.top) < 10:
                # if player is on top of platform it will create new platforms and move screen...
                self.game.new_platform()
                # makes the screen scroll once the player gets on top of platform as he goes upward...
                self.game.scroll_screen()
                self.game.score += 1  # Adjust the score or perform other actions as needed...
            print("i can jump", self.game.score)
        else:
            self.vel.y = -PLAYER_JUMP
        mob_hits = pg.sprite.spritecollide(self, self.game.all_mobs, True)
        if mob_hits:
            print("enemy down")
            self.game.score += 1
            print("Score:", self.game.score)
            # when player collides with mob and mob is killed it will respawn another mob randomly to make up for loss or of previous mobs to never run out of mobs...
            new_mob = Mob(randint(0, WIDTH), randint(0, HEIGHT/2), 20, 20, "normal")
            self.game.all_sprites.add(new_mob)
            self.game.all_mobs.add(new_mob)
        if hits:
            self.vel.y = -PLAYER_JUMP
            self.can_jump = False
            if self.vel.y > 0 and (self.rect.bottom - hits(0).rect.top) < 10:
                self.game.new_platform()
                self.game.scroll_screen()

    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # if friction - apply here...
        self.acc.x += self.vel.x * -PLAYER_FRIC
        # self.acc.y += self.vel.y * -0.3...
        # equations of motion...
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.vel.y == 0:
            self.can_jump = True

# platforms

class Platform(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.category = category
        self.speed = 0
        if self.category == "moving":
            self.speed = 2.5
    def update(self):
        if self.category == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed
        # scroll platforms upwards...
        self.rect.y -= SCROLL_SPEED
        if self.rect.bottom < 0:
            self.rect.y = HEIGHT
        if self.category == "bottom":
            self.rect.y = HEIGHT - BOTTOM_PLATFORM_HEIGHT

class Mob(Sprite):
    def __init__(self, x, y, w, h, kind):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(WIDTH/2, HEIGHT/2)

    def update(self):
        # makes the mobs move left to right and return on left side of screen...
        self.rect.x += MOB_SPEED
        if self.rect.left > WIDTH:
            self.rect.left = 0
        pass
