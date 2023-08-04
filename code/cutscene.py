import pygame
from state import State
from settings import *

class Cutscene0(State):
	def __init__(self, game, zone):
		State.__init__(self, game)

		self.zone = zone
		self.opening = True

		self.bar_height = 0
		self.target_height = HEIGHT * 0.1
		self.blackbar = pygame.Surface((WIDTH, self.bar_height))
		self.target = pygame.math.Vector2(self.zone.target.rect.center)
		self.new_pos = pygame.math.Vector2()

		self.timer = 0

	def move_camera(self):
		self.target.x += (self.new_pos.x - self.target.x)/200
		self.target.y += (self.new_pos.y - self.target.y)/200
		
	def blackbars(self, screen):
		
		if not self.opening:
		    self.bar_height -= (self.target_height - self.bar_height) / 60

		    if self.bar_height <= 0:
		        self.bar_height = 0
		        self.opening = True
		        self.exit_state()

		elif self.bar_height < self.target_height - 1:  
		    self.bar_height += (self.target_height - self.bar_height) / 60

		pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, self.bar_height))
		pygame.draw.rect(screen, BLACK, (0, HEIGHT - self.bar_height, WIDTH, self.target_height))

	def sequence(self):

		if self.timer < 60:
			self.target = pygame.math.Vector2(self.zone.target.rect.center)

		# move the camera new position after short cooldown above
		elif self.timer < 120:
			self.new_pos = pygame.math.Vector2(self.zone.npc.rect.center)
		elif self.timer < 180:
			self.new_pos = pygame.math.Vector2(self.zone.target.rect.center)
		elif self.timer < 240:
			self.new_pos = pygame.math.Vector2(RES)
		elif self.timer < 300:
			self.new_pos = pygame.math.Vector2(self.zone.npc.rect.center)

		# set the camera back to player before exiting cutscene
		elif self.timer < 360:
			self.new_pos = pygame.math.Vector2(self.zone.target.rect.center)

		elif self.timer > 420:
			self.opening = False


	def update(self, dt):
		self.game.reset_keys()
		self.timer += dt
		self.prev_state.update(dt)


	def render(self, screen):

		self.move_camera()
		self.sequence()
		self.prev_state.rendered_sprites.offset_draw(self.target)
		self.blackbars(screen)


class Cutscene1(Cutscene0):

	def sequence(self):

		if self.timer < 60:
			self.target = pygame.math.Vector2(self.zone.target.rect.center)

		# move the camera new position after short cooldown above
		elif self.timer < 120:
			self.new_pos = pygame.math.Vector2(0,0)
		elif self.timer < 180:
			self.new_pos = pygame.math.Vector2(self.zone.target.rect.center)
		elif self.timer < 240:
			self.new_pos = pygame.math.Vector2(self.zone.npc.rect.center)
		elif self.timer < 300:
			self.new_pos = pygame.math.Vector2(RES)

		# set the camera back to player before exiting cutscene
		elif self.timer < 360:
			self.new_pos = pygame.math.Vector2(self.zone.target.rect.center)

		elif self.timer > 420:
			self.opening = False

	def update(self, dt):
		self.game.reset_keys()
		self.timer += dt
		self.prev_state.update(dt)

	def render(self, screen):

		self.move_camera()
		self.sequence()
		self.prev_state.rendered_sprites.offset_draw(self.target)
		self.blackbars(screen)
