# this file was created by: Daniel Csubak
# content from kids can code: http://kidscancode.org/blog/
# content from stack overflow: https://stackoverflow.com/questions/29269389/how-do-i-make-a-score-counter-for-my-game-in-python
# content from geeksforgeeks: https://www.geeksforgeeks.org/how-to-add-moving-platforms-in-pygame/
# content from youtube: https://www.youtube.com/watch?v=Fp1dudhdX8k
# content from youtube: https://www.youtube.com/watch?v=EY0bxfISQNc
# content from youtube: https://www.youtube.com/watch?v=_E7kE3Zuf3A
# content from person: Chris Cozort
# content from person: Liam Hare
# content from person: Kian McLaughlin

# game design goals:
# make mobs that are killed when player collides with them
# make working score counter
# make platforms generate randomly
# make another class
# make game scroll upwards
# make the mobs moving
# make mobs respawn once previous has been killed

# game rules:
# platforms will move upwards
# mobs will move diagonally to make minor challenge for player
# player can jump and move
# mobs can be killed
# score counter works when collisions occur
# platforms are solid and standable for player

# game feedback:
# when player collides with platform they are either obstructed or sit on top of platform
# when player collides with mobs they are killed and respawned
# when mobs are killed player recieves +1 on score counter
# if player collides with platform from beneath score will be reset

# game freedom:
# player is able to move freely
# player can collide with mobs
# player can collide with platforms

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *

vec = pg.math.Vector2

# setup asset folders here - images sounds etc...
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Game:
    def __init__(self):
        # init pygame and create a window...
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game...")
        self.clock = pg.time.Clock()
        self.running = True
    
    def new(self):
        # create a group for all sprites...
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        # instantiate classes...
        self.player = Player(self)
        # add instances to groups...
        self.all_sprites.add(self.player)
        for m in range(0,10):
            m = Mob(randint(0, WIDTH), randint(0, HEIGHT/2), 20, 20, "normal")
            self.all_sprites.add(m)
            self.all_mobs.add(m)
        self.bottom_platform = Platform(0, HEIGHT - BOTTOM_PLATFORM_HEIGHT, WIDTH, BOTTOM_PLATFORM_HEIGHT, "bottom")
        self.all_sprites.add(self.bottom_platform)
        self.all_platforms.add(self.bottom_platform)
        self.run()

    def new_platform(self):
        # defines max amount of possible platform entities at once...
        max_platforms = 10
        if len(self.all_platforms) < max_platforms:
            plat = Platform(randint(0, WIDTH - PLATFORM_WIDTH), HEIGHT - BOTTOM_PLATFORM_HEIGHT - PLATFORM_HEIGHT, PLATFORM_WIDTH, PLATFORM_HEIGHT, "static")
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)
      
    def run(self):
        self.playing = True
        time_since_last_platform = 0
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.scroll_screen()
            self.draw()
            # new platfrom created in timed interval...
            time_since_last_platform += self.clock.get_rawtime()
            if time_since_last_platform > 400:
                self.new_platform()
                time_since_last_platform = 0

    def scroll_screen(self):
         # Move all the mobs and platforms upwards for scrolling effect...
        for sprite in self.all_sprites:
            sprite.rect.y -= SCROLL_SPEED   
        for mob in self.all_mobs:
            mob.rect.y -= SCROLL_SPEED    
        for mob in self.all_mobs:
            if mob.rect.bottom < 0:
                mob.rect.y = HEIGHT
        self.bottom_platform.rect.y -= SCROLL_SPEED    

    def update(self):
        self.all_sprites.update()
        # this is what prevents the player from falling through the platform when falling down...
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.vel.x = hits[0].speed*1.5  
         # this prevents the player from jumping up through a platform...
        if self.player.vel.y < 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                print("ouch")
                self.score = 0
                if self.player.rect.bottom >= hits[0].rect.top - 1:
                    self.player.rect.top = hits[0].rect.bottom
                    self.player.acc.y = 5
                    self.player.vel.y = 0
        # deletes platforms once player has climbed enough for them to be out of view...
        for platform in self.all_platforms:
            if platform.rect.bottom < 0:
                platform.kill()

    def events(self):
        for event in pg.event.get():
        # check for closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                
    def draw(self):
        ############ Draw ################
        # draw the background screen...
        self.screen.fill(BLACK)
        # draw all sprites
        self.all_sprites.draw(self.screen)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH/2, HEIGHT/10)
        # buffer - after drawing everything, flip display...
        pg.display.flip()
    
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass

g = Game()
while g.running:
    g.new()

pg.quit()
