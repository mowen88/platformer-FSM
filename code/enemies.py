import pygame
from settings import *
from npc import NPC
from enemy_fsm import Fall

class Crab(NPC):
	def __init__(self, game, zone, name, groups, pos, z, block_sprites):
		super().__init__(game, zone, name, groups, pos, z, block_sprites)

		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.4)
		self.state = Fall(self)
		self.fric = -0.1
		self.acc_rate = 0.3

	def state_logic(self):
		new_state = self.state.state_logic(self)
		if new_state: self.state = new_state
		else: self.state

	def update(self, dt):
		self.state_logic()
		self.state.update(self, dt)

