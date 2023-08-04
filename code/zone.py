import pygame
from os import walk
from settings import *
from pytmx.util_pygame import load_pygame
from camera import Camera
from state import State
from dialogue import Dialogue
from cutscene import Cutscene0, Cutscene1
from sprites import CutsceneCollider, Tile, Platform, CircularPlatform, MovingPlatform
from player import Player
from npc import NPC

class Zone(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.game = game
		self.target = None

		# sprite groups
		self.rendered_sprites = Camera(self.game, self)
		self.updated_sprites = pygame.sprite.Group()
		self.cutscene_sprites = pygame.sprite.Group()
		self.block_sprites = pygame.sprite.Group()
		self.platform_sprites = pygame.sprite.Group()

		self.create_map()

		self.dialogue = Dialogue(self.game, self, self.player)
		self.cutscenes = self.get_cutscenes()

	def get_cutscenes(self):
		cutscenes = {Cutscene0(self.game, self):True, Cutscene1(self.game, self):True}
		for key, value in CUTSCENES.items():
			cutscenes.update({list(cutscenes.keys())[key]: value})
		return cutscenes

	def create_map(self):
		tmx_data = load_pygame(f'../zones/{self.game.current_zone}.tmx')

		for obj in tmx_data.get_layer_by_name('platforms'):
			if obj.name == 'horizontal': MovingPlatform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(2,0))
			if obj.name == 'vertical': MovingPlatform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(0,3))
			if obj.name == 'vertical_2': MovingPlatform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(0,2))
			if obj.name == 'vertical_3': MovingPlatform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(0,2))
			if obj.name == 'vertical_4': MovingPlatform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(0,2))

		for obj in tmx_data.get_layer_by_name('cutscenes'):
			if obj.name == '0': CutsceneCollider([self.cutscene_sprites, self.updated_sprites], (obj.x, obj.y, obj.width, obj.height), obj.name)
			if obj.name == '1': CutsceneCollider([self.cutscene_sprites, self.updated_sprites], (obj.x, obj.y, obj.width, obj.height), obj.name)
		# # add backgrounds
		# Object(self.game, self, [self.rendered_sprites, Z_LAYERS[1]], (0,0), pygame.image.load('../assets/bg.png').convert_alpha())
		# Object(self.game, self, [self.rendered_sprites, Z_LAYERS[2]], (0,TILESIZE), pygame.image.load('../zones/0.png').convert_alpha())

		for x, y, surf in tmx_data.get_layer_by_name('blocks').tiles():
			Tile(self.game, self, [self.block_sprites, self.updated_sprites, self.rendered_sprites], (x * TILESIZE, y * TILESIZE), surf)

		# add the player
		for obj in tmx_data.get_layer_by_name('entities'):
			if obj.name == 'player': self.player = Player(self.game, self, obj.name, [self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], self.block_sprites)
			self.target = self.player

			if obj.name == 'guard': self.npc = NPC(self.game, self, obj.name, [self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], self.block_sprites)

	def get_distance(self, point_1, point_2):
		distance = (pygame.math.Vector2(point_2) - pygame.math.Vector2(point_1))
		return distance

	def start_cutscene(self):
		for sprite in self.cutscene_sprites:
			if self.player.hitbox.colliderect(sprite.rect):
				if list(self.cutscenes.values())[sprite.number]:
					list(self.cutscenes.keys())[sprite.number].enter_state()
					self.cutscenes.update({list(self.cutscenes.keys())[sprite.number]: False})


	def update(self, dt):
		if ACTIONS['return']: 
			pass
			self.game.reset_keys()
		
		self.updated_sprites.update(dt)
		self.rendered_sprites.screenshake_update(dt)

		self.start_cutscene()

	def render(self, screen):
		screen.fill(LIGHT_GREY)
		self.rendered_sprites.offset_draw(self.target.rect.center)
		self.game.render_text(str(round(self.game.clock.get_fps(), 2)), WHITE, self.game.small_font, (HALF_WIDTH, TILESIZE))
		self.game.render_text(self.player.pos, WHITE, self.game.small_font, RES/2)