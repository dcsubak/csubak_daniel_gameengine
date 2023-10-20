# This file was created by: Daniel Csubak
# Content from Chris Bradfield; Kids Can Code
# Video link: https:///youtu.be/OmlQ0XCvIn0
 
# game settings 
WIDTH = 360
HEIGHT = 480
FPS = 60
SCORE = 0

# player settings
PLAYER_JUMP = 30
PLAYER_GRAV = 1.5
global PLAYER_FRIC
PLAYER_FRIC = 0.3

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

 
PLATFROM_LIST = [(0, HEIGHT - 40, WIDTH, 40, "ice"),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20, "normal"),
                 (125, HEIGHT - 350, 100, 20, "moving")
                 (350,200, 100, 20, "normal"),
                 (175, 100, 50, 20, "normal")]