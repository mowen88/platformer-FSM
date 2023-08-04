import pygame
from state import State
from settings import *
from dialogue import Dialogue

class Cutscene0(State):
	def __init__(self, game, zone, number):
		State.__init__(self, game)

		self.zone = zone
		self.number = number
		self.opening = True

		self.bar_height = 0
		self.target_height = HEIGHT * 0.1
		self.blackbar = pygame.Surface((WIDTH, self.bar_height))
		self.target = pygame.math.Vector2(self.zone.target.rect.center)
		self.new_pos = pygame.math.Vector2()

		self.timer = 0

		self.dialogue_active = False

	def create_dialogue(self, target_sprite, number):
		self.dialogue = Dialogue(self.game, self.zone, target_sprite, number)
		self.dialogue_active = True

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
			self.create_dialogue(self.zone.target, self.number)
			self.new_pos = pygame.math.Vector2(self.zone.npc.rect.center)
		elif self.timer < 180:
			self.new_pos = pygame.math.Vector2(self.zone.target.rect.center)
		elif self.timer < 240:
			self.dialogue_active = False
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
		self.prev_state.rendered_sprites.offset_draw(self.target)
		self.sequence()
		if self.dialogue_active:
			self.dialogue.render(screen)
		self.blackbars(screen)

class Cutscene1(Cutscene0):

	def sequence(self):

		if self.timer < 90:
			self.target = pygame.math.Vector2(self.zone.target.rect.center)

		# move the camera new position after short cooldown above
		elif self.timer < 180:
			self.new_pos = pygame.math.Vector2(0,0)
			self.create_dialogue(self.zone.target, self.number)
		elif self.timer < 270:
			self.new_pos = pygame.math.Vector2(self.zone.target.rect.center)
		elif self.timer < 360:
			self.new_pos = pygame.math.Vector2(self.zone.npc.rect.center)
		elif self.timer < 450:
			self.new_pos = pygame.math.Vector2(RES)

		# set the camera back to player before exiting cutscene
		elif self.timer < 540:
			self.new_pos = pygame.math.Vector2(self.zone.target.rect.center)

		elif self.timer > 630:
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
