import pygame, csv
from settings import *
from camera import Camera
from state import State
from create_zone import CreateZone

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

		self.scene = CreateZone(self.game, self)
		self.scene.create()
		self.cutscenes = self.scene.get_cutscenes()
		self.cutscene_running = False

	def restart_zone(self, zone):
		Zone(self.game, zone, self.entry_point).enter_state()

	def get_zone_size(self):
		with open(f'../zones/{self.game.current_zone}/{self.game.current_zone}.csv', newline='') as csvfile:
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
		self.game.render_text(self.npc.move, WHITE, self.game.small_font, RES/2)
