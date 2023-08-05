import pygame

FPS = 60
TILESIZE = 20
RES = WIDTH, HEIGHT = pygame.math.Vector2(400, 225)#(640, 360)#(960, 540)
HALF_WIDTH, HALF_HEIGHT = RES/2

FONT = '../fonts/Pokemon Classic.ttf'

LAYERS = {
	'BG0': 0,
	'BG1': 1,
	'BG2': 2,
	'Water': 3,
	'particles': 4,
	'NPCs': 5,
	'player':6,
	'weapons': 7,
	'blocks': 8,
	'explosions': 9,
	'foreground': 10
}

CUTSCENES = {0: True, 1: True}

DIALOGUE = {
			0: ['This is the first line','for cutscene 0 dialogue.','Can we have another line?'], 
			1: ['this is dialogue for cutscene 1']
			}


# key events
ACTIONS = {'escape': False, 'space': False, 'up': False, 'down': False, 'left': False,
			'right': False, 'return': False, 'backspace': False, 'left_click': False, 
			'right_click': False, 'scroll_up': False, 'scroll_down': False}

# game colours
BLACK = ((39, 39, 39))
GREY = ((91,83,145))
LIGHT_GREY = ((146, 143, 184))
WHITE = ((229, 229, 229)) 
BLUE = ((20, 68, 145))
LIGHT_BLUE = ((113, 181, 219))
RED = ((112, 21, 31))
ORANGE = ((227, 133, 36))
RED_ORANGE = ((255, 130, 99)) 
PINK = ((195, 67, 92))
GREEN = ((88, 179, 150))
LIGHT_GREEN = ((106, 226, 145))
PURPLE = ((66, 0, 78))
CYAN = ((0, 255, 255))
MAGENTA = ((153, 60, 139))
YELLOW = ((224, 225, 146))