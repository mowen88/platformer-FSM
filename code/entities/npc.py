from settings import *
from entities.physics_object import Entity

class NPC(Entity):
	def __init__(self, game, zone, name, groups, pos, z):
		super().__init__(game, zone, name, groups, pos, z)
		
		# animation
		self.name = name
		self.animations = {'lunge':[], 'shoot':[], 'telegraph':[],'attack':[], 'idle':[], 'run':[], 'skid':[], 'land':[], 'jump':[], 'double_jump':[], 'fall':[]}
		self.animation_type = ''
		self.import_images(self.animations)
		self.frame_index = 0
		self.original_image = self.animations['idle'][self.frame_index]
		self.image = self.original_image
		self.facing = 1

		# self.image = pygame.Surface((TILESIZE * 2, TILESIZE * 3))
		# self.image.fill(RED)
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.2)
		self.old_hitbox = self.hitbox.copy()

		# physics
		self.move = {'right':False, 'left':False}
		self.angle = 0
		self.target_angle = 0
		self.acc_rate = 0.5
		self.fric = -0.2
		self.acc = pygame.math.Vector2(0, 0)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.vel = pygame.math.Vector2()
		self.platform_speed = pygame.math.Vector2()
		
		# jumping
		self.jump_height = 7
		self.max_fall_speed = 7

		# state specific
		self.on_ground = False
		self.state = Fall(self)
		

	def import_images(self, animation_states):

		path = f'../assets/{self.name}/'

		for animation in animation_states.keys():
			full_path = path + animation
			animation_states[animation] = self.game.get_folder_images(full_path)

	def animate(self, state, animation_speed, loop = True):

		self.frame_index += animation_speed
		if not loop and self.frame_index >= len(self.animations[state])-1:
			self.frame_index = len(self.animations[state])-1
		else:
			self.frame_index = self.frame_index % len(self.animations[state])	

		right_image = pygame.transform.flip(self.animations[state][int(self.frame_index)], self.facing, False)
		self.angle += (-(self.vel.x * 3) - self.angle)/10
		self.image = pygame.transform.rotate(right_image, self.angle)
		self.rect = self.image.get_rect(center = self.rect.center)

	def move_logic(self):
		if self.move['right']:
			self.move['left'] = False
			self.acc.x += self.acc_rate
			self.target_angle = self.vel.x * 10
		elif self.move['left']:
			self.move['right'] = False
			self.acc.x -= self.acc_rate
			self.target_angle = self.vel.x * 10
		else:
			self.move['right'], self.move['left'] = False, False 
			self.target_angle = 0

		if self.vel.x > 0:
			self.facing = 0
		else:
			self.facing = 1

	def switch_direction(self):
		self.vel.x = 0
		if self.move['right']:
			self.move['right'], self.move['left'] = False, True
		else:
			self.move['left'], self.move['right'] = False, True

	def platforms(self, group, dt):

		for platform in group.copy():
			platform_raycast = pygame.Rect(platform.rect.x, platform.rect.y - 4, platform.rect.width, platform.rect.height)
			if self.hitbox.colliderect(platform.rect) or self.hitbox.colliderect(platform_raycast): 
				if self.hitbox.bottom <= platform.rect.top + 4 and self.vel.y >= 0:
					self.platform_vel = platform.pos - platform.old_pos
					self.hitbox.bottom = platform.rect.top
					self.on_ground = True
					self.vel.y = 0

					self.rect.centery = self.hitbox.centery
					self.pos.y = self.hitbox.centery

					self.pos.x += self.platform_vel.x


	def collisions(self, direction):

		for sprite in self.zone.block_sprites:
			if self.hitbox.colliderect(sprite.hitbox): 
				if direction == 'x':
					if self.hitbox.right >= sprite.hitbox.left and self.old_hitbox.right <= sprite.old_hitbox.left:
						self.hitbox.right = sprite.hitbox.left
					
					elif self.hitbox.left <= sprite.hitbox.right and self.old_hitbox.left >= sprite.old_hitbox.right:
						self.hitbox.left = sprite.hitbox.right

								
					self.rect.centerx = self.hitbox.centerx
					self.pos.x = self.hitbox.centerx

					self.switch_direction()
					
				if direction == 'y':
					if self.hitbox.bottom >= sprite.hitbox.top and self.old_hitbox.bottom <= sprite.old_hitbox.top:
						self.hitbox.bottom = sprite.hitbox.top
						self.on_ground = True
						self.vel.y = 0
			
					elif self.hitbox.top <= sprite.hitbox.bottom and self.old_hitbox.top >= sprite.old_hitbox.bottom:
						self.hitbox.top = sprite.hitbox.bottom
						self.vel.y = 0

					self.rect.centery = self.hitbox.centery
					self.pos.y = self.hitbox.centery

	def jump(self, height):
		self.vel.y = -height

	def physics_x(self, dt):

		self.old_hitbox = self.hitbox.copy()

		self.acc.x += self.vel.x * self.fric
		self.vel.x += self.acc.x * dt
		
		self.pos.x += self.vel.x * dt + (0.5 * self.acc.x) * (dt**2)

		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		
		self.collisions('x')
		self.platforms(self.zone.platform_sprites, dt)

		# if npc is going slow enough, make the npc stand still
		#if abs(self.vel.x) < 0.1: self.vel.x = 0

	def physics_y(self, dt):

		self.vel.y += self.acc.y * dt

		self.pos.y += self.vel.y * dt + (0.5 * self.acc.y) * dt
		self.hitbox.centery = round(self.pos.y)
		self.collisions('y')
		self.rect.centery = self.hitbox.centery

		# limit max fall speed
		if self.vel.y >= self.max_fall_speed: 
			self.vel.y = self.max_fall_speed

		# Make the npc off ground if moving in y direction
		if abs(self.vel.y) >= 0.5: 
			self.on_ground = False

		# apply gravity always
		self.acc.y = self.zone.gravity

	def state_logic(self):
		new_state = self.state.state_logic(self)
		if new_state: self.state = new_state
		else: self.state

	def update(self, dt):
		self.state_logic()
		self.state.update(self, dt)

class Idle:
	def __init__(self, npc):
		
		npc.frame_index = 0

	def state_logic(self, npc):

		if not npc.on_ground:
			return Fall(npc)

		if npc.move['right']:
			npc.acc.x += 0.5
			npc.facing = 0
			npc.target_angle = -10
			return Move(npc)

		elif npc.move['left']:
			npc.acc.x -= 0.5
			npc.facing = 1
			npc.target_angle = 10
			return Move(npc)

	def update(self, npc, dt):
	
		npc.acc.x = 0
		npc.physics_x(dt)
		npc.physics_y(dt)
		npc.animate('idle', 0.2 * dt)

class Move(Idle):

	def state_logic(self, npc):

		if not npc.on_ground:
			return Fall(npc)

		if not (npc.move['right'] or npc.move['left']) and abs(npc.vel.x) <= 0.1:
			return Idle(npc)

	def update(self, npc, dt):

		npc.acc.x = 0
		npc.move_logic()
		npc.physics_x(dt)
		npc.physics_y(dt)

		if (npc.vel.x > 0 and not npc.move['right']) or (npc.vel.x < 0 and not npc.move['left']):
			npc.animate('skid', 0.2 * dt)
		else:
			npc.animate('run', 0.2 * dt)

class Landing(Idle):



	def state_logic(self, npc):

		if npc.frame_index > len(npc.animations['land'])-1:
			return Idle(npc)

	def update(self, npc, dt):

		npc.acc.x = 0
		npc.move_logic()
		npc.physics_x(dt)
		npc.physics_y(dt)

		npc.animate('land', 0.2 * dt)

class Fall(Idle):

	def state_logic(self, npc):

		if npc.on_ground:
			return Landing(npc)

	def update(self, npc, dt):
		npc.acc.x = 0
		npc.move_logic()
		npc.physics_x(dt)
		npc.physics_y(dt)
		npc.animate('fall', 0.2 * dt, False)



		


		
		