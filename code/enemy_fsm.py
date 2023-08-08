import pygame
from settings import *

class Idle:
	def __init__(self, enemy):
		
		enemy.frame_index = 0
		self.timer = 0

	def state_logic(self, enemy):

		if self.timer > 240:
			enemy.move['right'] = True

		if not enemy.on_ground:
			return Fall(enemy)

		if enemy.move['right']:
			enemy.acc.x += 0.5
			enemy.facing = 0
			enemy.target_angle = -10
			return Move(enemy)

		elif enemy.move['left']:
			enemy.acc.x -= 0.5
			enemy.facing = 1
			enemy.target_angle = 10
			return Move(enemy)

	def update(self, enemy, dt):
		self.timer += dt
	
		enemy.acc.x = 0
		enemy.physics_x(dt)
		enemy.physics_y(dt)
		enemy.animate('idle', 0.2 * dt)

class Move:
	def __init__(self, enemy):
		
		enemy.frame_index = 0

	def state_logic(self, enemy):

		if not enemy.on_ground:
			return Fall(enemy)


		if not (enemy.move['right'] or enemy.move['left']) and abs(enemy.vel.x) <= 0.1:
			return Idle(enemy)

	def update(self, enemy, dt):

		enemy.acc.x = 0
		enemy.move_logic()
		enemy.physics_x(dt)
		enemy.physics_y(dt)

		if (enemy.vel.x > 0 and not enemy.move['right']) or (enemy.vel.x < 0 and not enemy.move['left']):
			enemy.animate('skid', 0.2 * dt)
		else:
			enemy.animate('run', 0.2 * dt)

class Landing:
	def __init__(self, enemy):
		
		enemy.frame_index = 0

	def state_logic(self, enemy):

		if enemy.frame_index > len(enemy.animations['land'])-1:
			return Idle(enemy)

	def update(self, enemy, dt):

		enemy.acc.x = 0
		enemy.move_logic()
		enemy.physics_x(dt)
		enemy.physics_y(dt)

		enemy.animate('land', 0.2 * dt)

class Fall:
	def __init__(self, enemy):
		
		enemy.frame_index = 0

	def state_logic(self, enemy):

		if enemy.on_ground:
			return Landing(enemy)

	def update(self, enemy, dt):
		enemy.acc.x = 0
		enemy.move_logic()
		enemy.physics_x(dt)
		enemy.physics_y(dt)
		enemy.animate('fall', 0.2 * dt, False)