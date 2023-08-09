import pygame
from settings import *
from npc import NPC
from enemy_fsm import Fall

class Crab(NPC):
	def __init__(self, game, zone, name, groups, pos, z):
		super().__init__(game, zone, name, groups, pos, z)

		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.4)
		self.state = Fall(self)
		self.fric = -0.1
		self.acc_rate = 0.2
		self.vision_rect = pygame.Rect(0,0, 5 * TILESIZE, self.rect.height)
		
	def vision_box(self):
		if self.facing == 0:
			self.vision_rect.midleft = self.rect.center# - self.offset
		else:
			self.vision_rect.midright = self.rect.center# - self.offset

	def state_logic(self):
		new_state = self.state.state_logic(self)
		if new_state: self.state = new_state
		else: self.state

	def update(self, dt):
		self.vision_box()
		self.state_logic()
		self.state.update(self, dt)

	def render(self,screen):
		pygame.draw.rect(screen, WHITE, self.vision_rect, 2)



