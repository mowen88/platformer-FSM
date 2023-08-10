import pygame, random
from settings import *
from entities.npc import NPC

class Crab(NPC):
	def __init__(self, game, zone, name, groups, pos, z):
		super().__init__(game, zone, name, groups, pos, z)

		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.4, -self.rect.height * 0.4)
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

class Idle:
	def __init__(self, enemy):
		
		self.timer = 0
		# get a random time between 0 and 300
		self.time = self.random_wait(300)

	def random_wait(self, multiple):
		return random.random() * multiple

	def start_stop(self, enemy):
		# when this is called, if enemy is still, it will start moving, otherwise it will stop
		if self.timer > self.time:
			self.timer = 0
			if abs(enemy.vel.x) < 0.1:
				# set vel x to 0 to stop them sliding against wall
				enemy.vel.x = 0
				if enemy.facing == 1:
					enemy.move['left'] = True
				else:
					enemy.move['right'] = True
			else:
				#reset moving left and right to false
				enemy.move.update({key: False for key in enemy.move})
	def state_logic(self, enemy):

		# hit player if close
		if enemy.zone.get_distance(enemy.hitbox.center, enemy.zone.target.hitbox.center) <= 40\
		and enemy.name == 'guard':
			return Lunge(enemy)

		# if see player, go into into telegraph, then attack
		if enemy.zone.target.hitbox.colliderect(enemy.vision_rect):
			return Telegraph(enemy)

		self.start_stop(enemy)

		if not enemy.on_ground:
			return Fall(enemy)

		if enemy.move['right']:
			# enemy.acc.x += 0.5
			# enemy.facing = 0
			# enemy.target_angle = -10
			return Move(enemy)

		elif enemy.move['left']:
			# enemy.acc.x -= 0.5
			# enemy.facing = 1
			# enemy.target_angle = 10
			return Move(enemy)

	def update(self, enemy, dt):
		self.timer += dt
		enemy.acc.x = 0
		enemy.physics_x(dt)
		enemy.physics_y(dt)
		enemy.animate('idle', 0.2 * dt)

class Move(Idle):

	def state_logic(self, enemy):

		# hit player if close
		if enemy.zone.get_distance(enemy.hitbox.center, enemy.zone.target.hitbox.center) <= 40\
		and enemy.name == 'guard':
			return Lunge(enemy)

		if enemy.zone.target.hitbox.colliderect(enemy.vision_rect):
			return Telegraph(enemy)

		self.start_stop(enemy)

		if not enemy.on_ground:
			return Fall(enemy)

		if not (enemy.move['right'] or enemy.move['left']) and abs(enemy.vel.x) <= 0.1:
			return Idle(enemy)

	def update(self, enemy, dt):
		self.timer += dt
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

class Telegraph:
	def __init__(self, enemy):
		
		enemy.frame_index = 0

	def state_logic(self, enemy):

		if enemy.frame_index > len(enemy.animations['telegraph'])-1:
			if enemy.name == 'crab':
				return Attack(enemy)
			else:
				return Shoot(enemy)

	def update(self, enemy, dt):

		enemy.acc.x = 0
		enemy.physics_x(dt)
		enemy.physics_y(dt)
		enemy.animate('telegraph', 0.2 * dt)

class Attack(Fall):
	def __init__(self, enemy):
		
		self.timer = 30
		self.speed = 8 * self.direction(enemy)
		enemy.vel.x = self.speed
		# jump slightly when attacking
		enemy.vel.y = -4

	def direction(self, enemy):
		if enemy.facing == 0:
			return 1
		else:
			return -1

	def state_logic(self, enemy):

		if not enemy.alive:
			return Death(enemy)

		if self.timer <= 0:
			return Idle(enemy)

	def update(self, enemy, dt):

		self.timer -= dt

		enemy.acc.x = 0
		enemy.vel.x = self.speed
		self.speed -= self.direction(enemy) * dt * 0.3
		enemy.physics_x(dt)
		# add y physics to apply gravity to the jump
		enemy.physics_y(dt)

		enemy.animate('attack', 0.2 * dt)



