import pygame
from settings import *

class Idle:
	def __init__(self, player):
		
		player.frame_index = 0

	def state_logic(self, player):

		if not player.on_ground:
			return Fall(player)

		if player.move['right']:
			player.acc.x += 0.5
			player.facing = 0
			player.target_angle = -10
			return Move(player)

		elif player.move['left']:
			player.acc.x -= 0.5
			player.facing = 1
			player.target_angle = 10
			return Move(player)

	def update(self, player, dt):
	
		player.acc.x = 0
		player.physics_x(dt)
		player.physics_y(dt)
		player.animate('idle', 0.2 * dt)

class Move(Idle):

	def state_logic(self, player):

		if not player.on_ground:
			return Fall(player)

		if not (player.move['right'] or player.move['left']) and abs(player.vel.x) <= 0.1:
			return Idle(player)

	def update(self, player, dt):

		player.acc.x = 0
		player.move_logic()
		player.physics_x(dt)
		player.physics_y(dt)

		if (player.vel.x > 0 and not player.move['right']) or (player.vel.x < 0 and not player.move['left']):
			player.animate('skid', 0.2 * dt)
		else:
			player.animate('run', 0.2 * dt)

class Landing(Idle):

	def state_logic(self, player):

		if player.frame_index > len(player.animations['land'])-1:
			return Idle(player)

	def update(self, player, dt):

		player.acc.x = 0
		player.move_logic()
		player.physics_x(dt)
		player.physics_y(dt)

		player.animate('land', 0.2 * dt)

class Fall(Idle):

	def state_logic(self, player):

		if player.on_ground:
			return Landing(player)

	def update(self, player, dt):
		player.acc.x = 0
		player.move_logic()
		player.physics_x(dt)
		player.physics_y(dt)
		player.animate('fall', 0.2 * dt, False)