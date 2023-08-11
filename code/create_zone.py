import pygame
from os import walk
from settings import *
from pytmx.util_pygame import load_pygame
from cutscene import Cutscene0, Cutscene1
from sprites import Collider, CutsceneCollider, BG, Tile, AnimatedTile, DisappearingPlatform, EscalatorPlatform, MovingPlatform, SawBlade
from entities.player import Player
from entities.physics_object import Entity, Box
from entities.npc import NPC
from entities.crab import Crab
from entities.guard import Guard

class CreateZone:
	def __init__(self, game, zone):
		self.game = game
		self.zone = zone

	def get_cutscenes(self):
		cutscenes = {Cutscene0(self.game, self.zone, 0):True, Cutscene1(self.game, self.zone, 1):True}
		for key, value in CUTSCENES.items():
			cutscenes.update({list(cutscenes.keys())[key]: value})
		return cutscenes

	def create(self):
		tmx_data = load_pygame(f'../zones/{self.game.current_zone}/{self.game.current_zone}.tmx')
		for x, y, surf in tmx_data.get_layer_by_name('blocks').tiles():
			Tile(self.game, self.zone, [self.zone.block_sprites, self.zone.rendered_sprites], (x * TILESIZE, y * TILESIZE), surf)

		# key is the platform name in tmx, value is a list, containing the direction and amplitude
		platforms = {'horizontal':[(0.3,0.0), 75], 'horizontal_2':[(-0.3,0.0), 75], 'vertical':[(0.0,-0.2), 120], 'vertical_2':[(0.0, 0.3), 75], 'vertical_3':[(0.0,0.2), 90], 'vertical_4':[(0.0,0.3), 90]}

		for obj in tmx_data.get_layer_by_name('platforms'):
			for key, value in platforms.items():
				if obj.name == key: MovingPlatform(self.game, self.zone, [self.zone.platform_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=value[0], amplitude=value[1])

		# add the player
		for obj in tmx_data.get_layer_by_name('entities'):
			if obj.name == 'player':
				self.zone.player = Player(self.game, self.zone, obj.name, [self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'])
				self.zone.target = self.zone.player

			if obj.name == 'crab': self.zone.crab = Crab(self.game, self.zone, obj.name, [self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'])
			if obj.name == 'guard': self.zone.npc = Guard(self.game, self.zone, obj.name, [self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'])
			if obj.name == 'block': Box(self.game, self.zone, obj.name, [self.zone.pushable_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'])


		for obj in tmx_data.get_layer_by_name('hazards'):
			if obj.name == 'horizontal': SawBlade(self.game, self.zone, [self.zone.sawblade_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(0.5,0.0), amplitude=60)
			# if obj.name == 'horizontal_2': SawBlade(self.game, self.zone, [self.zone.sawblade_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(-0.5,0.0), amplitude=60)
			# if obj.name == 'vertical': SawBlade(self.game, self.zone, [self.zone.sawblade_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(0.0,0.5), amplitude=60)
			
			# escalator platforms
			if obj.name == 'escalator_right': EscalatorPlatform(self.game, self.zone, [self.zone.platform_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], pos=(obj.x, obj.y), surf=f'../assets/hazards/escalator_platform/', direction=(1.0,0.0), amplitude=75)
			if obj.name == 'escalator_left': EscalatorPlatform(self.game, self.zone, [self.zone.platform_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], pos=(obj.x, obj.y), surf=f'../assets/hazards/escalator_platform/', direction=(-1.0,0.0), amplitude=75)
			# spikes!!!
			if obj.name == 'spikes': AnimatedTile(self.game, self.zone, [self.zone.hazard_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], pos=(obj.x, obj.y), surf=f'../assets/hazards/{obj.name}/')
			# disappearing platforms
			if obj.name == 'disappearing_platform': DisappearingPlatform(self.game, self.zone, [self.zone.platform_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], pos=(obj.x, obj.y), surf=f'../assets/hazards/{obj.name}/')

		for obj in tmx_data.get_layer_by_name('cutscenes'):
			if obj.name == '0': CutsceneCollider([self.zone.cutscene_sprites, self.zone.updated_sprites], (obj.x, obj.y, obj.width, obj.height), obj.name)
			if obj.name == '1': CutsceneCollider([self.zone.cutscene_sprites, self.zone.updated_sprites], (obj.x, obj.y, obj.width, obj.height), obj.name)


		for obj in tmx_data.get_layer_by_name('edge_colliders'):
			Collider([self.zone.collision_sprites], (obj.x, obj.y, obj.width, obj.height))

				# add static image layers
		for _, __, img_files in walk(f'../zones/{self.game.current_zone}/bg_images'):
			for img in img_files:
				if img == '2x6_white.png': BG(self.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (0, 0), pygame.image.load(f'../zones/{self.game.current_zone}/bg_images/{img}').convert_alpha(), (0.1, 0.1), LAYERS['blocks'])
				if img == 'bg1.png': BG(self.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (0, 0), pygame.image.load(f'../zones/{self.game.current_zone}/bg_images/{img}').convert_alpha(), (0.01, 0.01), LAYERS['BG1'])
				if img == 'bg2.png': BG(self.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (0, 0), pygame.image.load(f'../zones/{self.game.current_zone}/bg_images/{img}').convert_alpha(), (0.02, 0.05), LAYERS['BG2'])
				if img == 'bg0.png': BG(self.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (0, 0), pygame.image.load(f'../zones/{self.game.current_zone}/bg_images/{img}').convert_alpha(), (0.1, 0.03), LAYERS['BG0'])
		