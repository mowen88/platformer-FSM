import pygame, csv
from settings import *
from camera import Camera
from state import State
from cutscene import Cutscene
from create_zone import CreateZone

class Zone(State):
	def __init__(self, game, name, entry_point):
		State.__init__(self, game)

		self.game = game
		self.name = name
		self.entry_point = entry_point
		self.gravity = 0.3
		self.size = self.get_zone_size()

		PLAYER_DATA.update({'current_zone': self.name, 'entry_pos': self.entry_point})
		COMPLETED_DATA['visited_zones'].append(self.name)

		# sprite groups
		self.updated_sprites = pygame.sprite.Group()
		self.rendered_sprites = Camera(self.game, self)

		self.exit_sprites = pygame.sprite.Group()
		self.cutscene_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()
		self.block_sprites = pygame.sprite.Group()
		self.pushable_sprites = pygame.sprite.Group()
		self.platform_sprites = pygame.sprite.Group()
		self.hazard_sprites = pygame.sprite.Group()
		self.sawblade_sprites = pygame.sprite.Group()

		self.scene = CreateZone(self.game, self)
		self.scene.create()

		self.cutscene_running = False
		self.entering = True
		self.exiting = False
		self.new_zone = None

	def restart_zone(self, zone):
		Zone(self.game, zone, self.entry_point).enter_state()

	def get_zone_size(self):
		with open(f'../zones/{self.name}/{self.name}.csv', newline='') as csvfile:
		    reader = csv.reader(csvfile, delimiter=',')
		    for row in reader:
		        rows = (sum (1 for row in reader) + 1)
		        cols = len(row)
		return (cols * TILESIZE, rows * TILESIZE)

	def get_distance(self, point_1, point_2):
		distance = (pygame.math.Vector2(point_2) - pygame.math.Vector2(point_1)).magnitude()
		return distance

	def start_cutscene(self):
		for sprite in self.cutscene_sprites:
			if self.player.hitbox.colliderect(sprite.rect) and sprite.number not in COMPLETED_DATA['cutscenes'] and not self.entering:
				COMPLETED_DATA['cutscenes'].append(sprite.number)
				self.target.move.update({key: False for key in self.target.move})
				self.cutscene_running = True
				Cutscene(self.game, self, sprite.number).enter_state()

	def exit(self):
		for sprite in self.exit_sprites:
			if self.player.hitbox.colliderect(sprite.rect):
				self.exiting = True
				self.cutscene_running = True
				self.new_zone = ZONE_DATA[self.name][str(sprite.number)]
				self.entry_point = str(sprite.number)						

	def update(self, dt):
		
		self.start_cutscene()
		self.exit()
		

		if ACTIONS['return']: 
			self.exit_state()
			self.game.reset_keys()
		
		if not self.cutscene_running:
			self.target.input()

		self.updated_sprites.update(dt)
		self.rendered_sprites.screenshake_update(dt)	

		# has to go after start cutscene and exit to make sure it fades first
		self.fade_surf.update(dt)

	def render(self, screen):
		screen.fill(BLACK)
		self.rendered_sprites.offset_draw(screen, self.target.rect.center)

		self.fade_surf.draw(screen)
		self.game.render_text(str(round(self.game.clock.get_fps(), 2)), WHITE, self.game.small_font, (HALF_WIDTH, TILESIZE))
		#self.game.render_text(self.cutscene_running, WHITE, self.game.small_font, (HALF_WIDTH, TILESIZE))
		self.game.render_text(self.target.vel.y, WHITE, self.game.small_font, RES/2)
