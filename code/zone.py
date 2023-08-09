import pygame, csv
from os import walk
from settings import *
from pytmx.util_pygame import load_pygame
from camera import Camera
from state import State
from cutscene import Cutscene0, Cutscene1
from sprites import Collider, CutsceneCollider, BG, Tile, AnimatedTile, DisappearingPlatform, EscalatorPlatform, MovingPlatform, SawBlade
from entities.player import Player
from entities.npc import Entity, Box, NPC
from entities.enemies import Crab

class Zone(State):
	def __init__(self, game, name, entry_point):
		State.__init__(self, game)

		self.game = game
		self.name = name
		self.entry_point = entry_point
		self.gravity = 0.3
		self.size = self.get_zone_size()

		# sprite groups
		self.updated_sprites = pygame.sprite.Group()
		self.rendered_sprites = Camera(self.game, self)
		
		self.cutscene_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()
		self.block_sprites = pygame.sprite.Group()
		self.pushable_sprites = pygame.sprite.Group()
		self.platform_sprites = pygame.sprite.Group()
		self.hazard_sprites = pygame.sprite.Group()
		self.sawblade_sprites = pygame.sprite.Group()

		self.create_map()

		self.cutscenes = self.get_cutscenes()
		self.cutscene_running = False

	def restart_zone(self, zone):
		Zone(self.game, zone, self.entry_point).enter_state()

	def get_cutscenes(self):
		cutscenes = {Cutscene0(self.game, self, 0):True, Cutscene1(self.game, self, 1):True}
		for key, value in CUTSCENES.items():
			cutscenes.update({list(cutscenes.keys())[key]: value})
		return cutscenes

	def get_zone_size(self):
		with open(f'../zones/0.csv', newline='') as csvfile:
		    reader = csv.reader(csvfile, delimiter=',')
		    for row in reader:
		        rows = (sum (1 for row in reader) + 1)
		        cols = len(row)
		return (cols * TILESIZE, rows * TILESIZE)

	def create_map(self):
		tmx_data = load_pygame(f'../zones/{self.game.current_zone}.tmx')

		# key is the platform name in tmx, value is a list, containing the direction and amplitude
		platforms = {'horizontal':[(0.3,0.0), 75], 'horizontal_2':[(-0.3,0.0), 75], 'vertical':[(0.0,-0.2), 120], 'vertical_2':[(0.0, 0.3), 75], 'vertical_3':[(0.0,0.2), 90], 'vertical_4':[(0.0,0.3), 90]}

		for obj in tmx_data.get_layer_by_name('platforms'):
			for key, value in platforms.items():
				if obj.name == key: MovingPlatform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=value[0], amplitude=value[1])
			# if obj.name == platforms: MovingPlatform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(0.3,0.0), amplitude=75)
			# if obj.name == 'horizontal_2': MovingPlatform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(0.3,0.0), amplitude=75)
			# if obj.name == 'vertical': MovingPlatform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(0.0,-0.2), amplitude=120)
			# if obj.name == 'vertical_2': MovingPlatform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(0.0, 0.3), amplitude=75)
			# if obj.name == 'vertical_3': MovingPlatform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(0.0,0.2), amplitude=90)
			# if obj.name == 'vertical_4': MovingPlatform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(0.0,0.3), amplitude=90)

		
		for obj in tmx_data.get_layer_by_name('hazards'):
			if obj.name == 'horizontal': SawBlade(self.game, self, [self.sawblade_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(0.5,0.0), amplitude=60)
			if obj.name == 'horizontal_2': SawBlade(self.game, self, [self.sawblade_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(-0.5,0.0), amplitude=60)
			if obj.name == 'vertical': SawBlade(self.game, self, [self.sawblade_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(0.0,0.5), amplitude=60)
			# escalator platforms
			if obj.name == 'escalator_right': EscalatorPlatform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=f'../assets/hazards/escalator_platform/', direction=(1.0,0.0), amplitude=75)
			if obj.name == 'escalator_left': EscalatorPlatform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=f'../assets/hazards/escalator_platform/', direction=(-1.0,0.0), amplitude=75)
			# spikes!!!
			if obj.name == 'spikes': AnimatedTile(self.game, self, [self.hazard_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=f'../assets/hazards/{obj.name}/')
			# disappearing platforms
			if obj.name == 'disappearing_platform': DisappearingPlatform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=f'../assets/hazards/{obj.name}/')

		for obj in tmx_data.get_layer_by_name('cutscenes'):
			if obj.name == '0': CutsceneCollider([self.cutscene_sprites, self.updated_sprites], (obj.x, obj.y, obj.width, obj.height), obj.name)
			if obj.name == '1': CutsceneCollider([self.cutscene_sprites, self.updated_sprites], (obj.x, obj.y, obj.width, obj.height), obj.name)
		# # add backgrounds
		# Object(self.game, self, [self.rendered_sprites, Z_LAYERS[1]], (0,0), pygame.image.load('../assets/bg.png').convert_alpha())
		# Object(self.game, self, [self.rendered_sprites, Z_LAYERS[2]], (0,TILESIZE), pygame.image.load('../zones/0.png').convert_alpha())
		for obj in tmx_data.get_layer_by_name('edge_colliders'):
			Collider([self.collision_sprites], (obj.x, obj.y, obj.width, obj.height))
		# add the player
		for obj in tmx_data.get_layer_by_name('entities'):
			if obj.name == 'player':
				self.player = Player(self.game, self, obj.name, [self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'])
				self.target = self.player

			if obj.name == 'guard': self.npc = NPC(self.game, self, obj.name, [self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'])
			if obj.name == 'crab': self.crab = Crab(self.game, self, obj.name, [self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'])
			if obj.name == 'block': Box(self.game, self, obj.name, [self.pushable_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'])

		for x, y, surf in tmx_data.get_layer_by_name('blocks').tiles():
			Tile(self.game, self, [self.block_sprites, self.rendered_sprites], (x * TILESIZE, y * TILESIZE), surf)

		# add static image layers
		for _, __, img_files in walk(f'../zones/{self.name}/bg_images'):
			for img in img_files:
				#if img == '2x6_white.png': BG(self.game, self, [self.updated_sprites, self.rendered_sprites], (0, 0), pygame.image.load(f'../zones/{self.name}/bg_images/{img}').convert_alpha(), (0.1, 0.1), LAYERS['blocks'])
				if img == 'bg1.png': BG(self.game, self, [self.updated_sprites, self.rendered_sprites], (0, 0), pygame.image.load(f'../zones/{self.name}/bg_images/{img}').convert_alpha(), (0.01, 0.01), LAYERS['BG1'])
				if img == 'bg2.png': BG(self.game, self, [self.updated_sprites, self.rendered_sprites], (0, 0), pygame.image.load(f'../zones/{self.name}/bg_images/{img}').convert_alpha(), (0.02, 0.05), LAYERS['BG2'])
				if img == 'bg0.png': BG(self.game, self, [self.updated_sprites, self.rendered_sprites], (0, 0), pygame.image.load(f'../zones/{self.name}/bg_images/{img}').convert_alpha(), (0.1, 0.03), LAYERS['BG0'])
		
	def get_distance(self, point_1, point_2):
		distance = (pygame.math.Vector2(point_2) - pygame.math.Vector2(point_1)).magnitude()
		return distance

	def start_cutscene(self):
		for sprite in self.cutscene_sprites:
			if self.player.hitbox.colliderect(sprite.rect):
				if list(self.cutscenes.values())[sprite.number]:
					self.cutscene_running = True
					list(self.cutscenes.keys())[sprite.number].enter_state()
					# set movement to false when entering cutscene to stop the player momentum
					self.target.move.update({key: False for key in self.target.move})
					# set cutscene to false when entering cutscene to stop it activating again
					self.cutscenes.update({list(self.cutscenes.keys())[sprite.number]: False})
					CUTSCENES.update({list(CUTSCENES.keys())[sprite.number]: False})
					return

	def update(self, dt):
		
		self.start_cutscene()

		if ACTIONS['return']: 
			self.exit_state()
			self.game.reset_keys()
		
		if not self.cutscene_running:
			self.target.input()

		self.updated_sprites.update(dt)
		self.rendered_sprites.screenshake_update(dt)

	def render(self, screen):
		screen.fill(BLACK)
		self.rendered_sprites.offset_draw(screen, self.target.rect.center)
		self.game.render_text(str(round(self.game.clock.get_fps(), 2)), WHITE, self.game.small_font, (HALF_WIDTH, TILESIZE))
		#self.game.render_text(self.player.state, WHITE, self.game.small_font, (HALF_WIDTH, TILESIZE))
		self.game.render_text(self.player.jump_buffer, WHITE, self.game.small_font, RES/2)
		pygame.draw.rect(screen, WHITE, self.crab.vision_rect, 2)