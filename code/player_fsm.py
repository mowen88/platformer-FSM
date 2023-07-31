import pygame
from settings import *

class Idle:
	def __init__(self, player):
		
		player.frame_index = 0
		player.jump_counter = 1

	def state_logic(self, player):

		if not player.on_ground:
			return Fall(player)

		if ACTIONS['up']:
			ACTIONS['up'] = False
			return Jumping(player)

		if ACTIONS['right']:
			player.acc.x += 0.5
			player.facing = 0
			player.target_angle = -10
			return Move(player)

		elif ACTIONS['left']:
			player.acc.x -= 0.5
			player.facing = 1
			player.target_angle = 10
			return Move(player)

	def update(self, player, dt):
	
		player.acc.x = 0
		player.physics_x(dt)
		player.physics_y(dt)
		player.animate('idle', 0.2 * dt)

class Move:
	def __init__(self, player):
		
		player.frame_index = 0
		player.jump_counter = 1

	def state_logic(self, player):

		if not player.on_ground:
			return Fall(player)

		if ACTIONS['up']:
			ACTIONS['up'] = False
			return Jumping(player)

		if not (ACTIONS['right'] or ACTIONS['left']) and abs(player.dir.x) <= 0.1:
			return Idle(player)

	def update(self, player, dt):

		player.acc.x = 0
		player.move()
		player.physics_x(dt)
		player.physics_y(dt)

		if (player.dir.x > 0 and not ACTIONS['right']) or (player.dir.x < 0 and not ACTIONS['left']):
			player.animate('skid', 0.2 * dt)
		else:
			player.animate('run', 0.2 * dt)

class Landing:
	def __init__(self, player):
		
		player.frame_index = 0
		player.jump_counter = 1

	def state_logic(self, player):

		if ACTIONS['up']:
			ACTIONS['up'] = False
			return Jumping(player)

		if player.frame_index > len(player.animations['land'])-1:
			return Idle(player)

	def update(self, player, dt):

		player.acc.x = 0
		player.move()
		player.physics_x(dt)
		player.physics_y(dt)

		player.animate('land', 0.2 * dt)

class Fall:
	def __init__(self, player):
		
		player.frame_index = 0

	def state_logic(self, player):

		if ACTIONS['up']:
			player.jump_buffer_active = True
			ACTIONS['up'] = False
			if player.jump_counter > 0:
				return DoubleJumping(player)

		if player.on_ground:
			if player.jump_buffer > 0:
				player.jump_counter = 1
				return Jumping(player)
			else:
				return Landing(player)

	def update(self, player, dt):

		player.acc.x = 0
		player.move()
		player.physics_x(dt)
		player.physics_y(dt)

		player.animate('idle', 0.2 * dt)

class Jumping:
	def __init__(self, player):

		player.frame_index = 0
		player.jump(player.jump_height)

	def state_logic(self, player):

		if player.dir.y >= 0:
			return Fall(player)

		if ACTIONS['up'] and player.jump_counter > 0:
			ACTIONS['up'] = False
			return DoubleJumping(player)

	def update(self, player, dt):

		player.acc.x = 0
		player.move()
		player.physics_x(dt)
		player.physics_y(dt)

		player.animate('idle', 0.2 * dt)

class DoubleJumping:
	def __init__(self, player):

		player.frame_index = 0
		player.jump_counter = 0
		player.jump(player.jump_height)

	def state_logic(self, player):

		if player.dir.y >= 0:
			return Fall(player)

	def update(self, player, dt):
		
		player.acc.x = 0
		player.move()
		player.physics_x(dt)
		player.physics_y(dt)

		player.animate('idle', 0.2 * dt)
		