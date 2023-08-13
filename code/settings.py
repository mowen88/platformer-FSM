import pygame

FPS = 60
TILESIZE = 20
RES = WIDTH, HEIGHT = pygame.math.Vector2(400, 225)#(640, 360)#(960, 540)
HALF_WIDTH, HALF_HEIGHT = RES/2

# FONT = '../fonts/Pokemon Classic.ttf'
FONT = '../fonts/Typori-Regular.ttf'
# FONT = '../fonts/square_block.ttf'

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

PLAYER_DATA = {'current_zone': 'medium', 'entry_pos': '0', 'keys': ['blue_door'], 'gun_index': 0, 'max_health': 4, 'max_juice': 99, 'heal_cost': 11, 'partial_healths': 0}
COMPLETED_DATA = {'visited_zones': [], 'cutscenes': []}

ZONE_DATA = {
	'start':{'0': 'medium'},
	'small':{'1': 'medium'},
	'medium':{'0': 'small'}
	}

DIALOGUE = {
			0: [['Dude, where the hell are','you going ?'],
				['Sorry pal, gotta go!','Places to go....','People to see....']], 
			1: [['This is more dialogue for','a second cutscene.','Tell me if it worked ?'], 
				['How do you expect me to','hear you from up there ?']],
			2: [['I am on my bike and loving it!', 'Whatcha think?'], 
				['Anyway. . . '],
				["It's time to get outta here!"]]
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
YELLOW = ((254, 255, 123))