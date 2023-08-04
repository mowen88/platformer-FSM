import pygame
from settings import *

class Idle:
	def __init__(self, player):
		
		player.frame_index = 0

	def state_logic(self, player):

		if not player.on_ground:
			return Fall(player)

	def update(self, player, dt):
	
		player.acc.x = 0
		player.physics_x(dt)
		player.physics_y(dt)
		player.animate('idle', 0.2 * dt)

class Landing:
	def __init__(self, player):
		
		player.frame_index = 0

	def state_logic(self, player):

		if player.frame_index > len(player.animations['land'])-1:
			return Idle(player)

	def update(self, player, dt):

		player.acc.x = 0
		player.move_logic()
		player.physics_x(dt)
		player.physics_y(dt)

		player.animate('land', 0.2 * dt)

class Fall:
	def __init__(self, player):
		
		player.frame_index = 0

	def state_logic(self, player):

		if player.on_ground:
			return Landing(player)

	def update(self, player, dt):

		player.acc.x = 0
		player.move_logic()
		player.physics_x(dt)
		player.physics_y(dt)

		player.animate('fall', 0.2 * dt, False)