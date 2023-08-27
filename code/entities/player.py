import pygame
from settings import *
from entities.physics_object import Entity
from entities.player_fsm import WakeUp, OnBikeIdling

class Player(Entity):
	def __init__(self, game, zone, name, groups, pos, z):
		super().__init__(game, zone, name, groups, pos, z)

		self.game = game
		self.zone = zone
		self.z = z
		self.block_sprites = self.zone.block_sprites
		self.pushable_sprites = self.zone.pushable_sprites
		self.platform_sprites = self.zone.platform_sprites
		self.hazard_sprites = self.zone.hazard_sprites
		self.sawblade_sprites = self.zone.sawblade_sprites

		# animation
		self.name = 'player'
		self.animations = {'on_bike_idle':[], 'on_bike':[], 'death':[], 'idle':[], 'run':[], 'skid':[], 'land':[], 'jump':[], 'double_jump':[], 'fall':[]}
		self.animation_type = ''
		self.import_images(self.animations)
		
		self.frame_index = 0
		self.original_image = self.animations['idle'][self.frame_index]
		self.image = self.original_image
		self.facing = 0

		# self.image = pygame.Surface((TILESIZE * 2, TILESIZE * 3))
		# self.image.fill(RED)
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.25)
		self.old_hitbox = self.hitbox.copy()

		# physics
		self.acc_rate = 0.5
		self.fric = -0.2
		self.acc = pygame.math.Vector2(0, self.zone.gravity)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.vel = pygame.math.Vector2()
		self.platform_vel = pygame.math.Vector2()

		# jumping
		self.jump_height = 6
		self.max_fall_speed = 6
		self.jump_counter = 0
		self.cyote_timer = 0
		self.cyote_timer_threshold = 6
		self.jump_buffer_active = False
		self.jump_buffer = 0
		self.jump_buffer_threshold = 6

		# player states
		self.move = {'right':True, 'left':False}
		self.angle = 0
		self.on_ground = False
		self.alive = True
		if not self.zone.name == 'start':
			self.state = WakeUp(self)
		else:
			self.state = OnBikeIdling(self)

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

		elif self.move['left']:
			self.move['right'] = False
			self.acc.x -= self.acc_rate
		else:
			self.move['right'], self.move['left'] = False, False 

		if self.vel.x > 0:
			self.facing = 0
		else:
			self.facing = 1

	def input(self):

		if ACTIONS['right']:
			self.move['right'] = True
			self.move['left'] = False
		elif ACTIONS['left']:
			self.move['left'] = True
			self.move['right'] = False
		else:
			self.move['right'] = False
			self.move['left'] = False

	def get_collide_list(self, group): 
		hitlist = []
		for sprite in group:
			if sprite.hitbox.colliderect(self.hitbox): hitlist.append(sprite)
		return hitlist

	def collide_hazards(self):
		hitlist = self.get_collide_list(self.hazard_sprites)
		if hitlist: 
			self.alive = False
		# using distance between centres for circular sprites
		for sprite in self.sawblade_sprites:
			# adjust the distance here to fine tune collisions
			distance = sprite.hitbox.width * 0.7 
			if self.zone.get_distance(sprite.hitbox.center, self.hitbox.center) <= distance:
				self.alive = False

	def collide_edges(self):
		for sprite in self.collision_sprites:
			if self.hitbox.colliderect(sprite.rect):
				if (self.facing == 0 and self.hitbox.centerx > sprite.rect.left) or\
				(self.facing == 1 and self.hitbox.centerx < sprite.rect.right):
					return True
		
	def platforms(self, group, dt):

		for platform in group.copy():
			ray_height = 4
			platform_raycast = pygame.Rect(platform.rect.x, platform.rect.y - ray_height, platform.rect.width, platform.rect.height)
			if self.hitbox.colliderect(platform.rect) or self.hitbox.colliderect(platform_raycast): 
				if self.hitbox.bottom <= platform.rect.top + ray_height and self.vel.y > 0:
					self.platform_vel = platform.pos - platform.old_pos
					self.hitbox.bottom = platform.rect.top
					self.on_ground = True
					self.vel.y = 0

					self.rect.centery = self.hitbox.centery
					self.pos.y = self.hitbox.centery

					# if not hasattr(self, 'prev_platform'):
					# 	self.prev_platform = platform
					# 	self.platform_vel.x = 0
					# else:
					# 	self.platform_vel.x = platform.pos.x - platform.old_pos.x
					# 	self.prev_platform = platform

					self.pos.x += self.platform_vel.x

	def collisions(self, direction):

		for sprite in self.block_sprites:
			if sprite.hitbox.colliderect(self.hitbox): 

				if direction == 'x':
					if self.hitbox.right >= sprite.hitbox.left and self.old_hitbox.right <= sprite.old_hitbox.left:
						self.hitbox.right = sprite.hitbox.left
					
					elif self.hitbox.left <= sprite.hitbox.right and self.old_hitbox.left >= sprite.old_hitbox.right:
						self.hitbox.left = sprite.hitbox.right

					self.rect.centerx = self.hitbox.centerx
					self.pos.x = self.hitbox.centerx

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


	def pushable_collisions(self, direction):

		for sprite in self.zone.pushable_sprites:
			if self.hitbox.colliderect(sprite.hitbox): 
				if direction == 'x':
					if self.hitbox.right >= sprite.hitbox.left and self.old_hitbox.right <= sprite.old_hitbox.left:
						sprite.hitbox.left = self.hitbox.right
						sprite.vel.x = self.vel.x * 2

					elif self.hitbox.left <= sprite.hitbox.right and self.old_hitbox.left >= sprite.old_hitbox.right:
						sprite.hitbox.right = self.hitbox.left
						sprite.vel.x = self.vel.x * 2

					self.rect.centerx = self.hitbox.centerx
					self.pos.x = self.hitbox.centerx
					# makes sure the pushable sprite does not go through the blocks
					sprite.collisions('x')

				if direction == 'y':
					
					if self.hitbox.bottom >= sprite.hitbox.top and self.old_hitbox.bottom <= sprite.old_hitbox.top:
						self.hitbox.bottom = sprite.hitbox.top
						self.on_ground = True
			
					elif self.hitbox.top <= sprite.hitbox.bottom and self.old_hitbox.top >= sprite.old_hitbox.bottom:
						self.hitbox.top = sprite.hitbox.bottom
						sprite.vel.y = self.vel.y

					self.rect.centery = self.hitbox.centery
					self.pos.y = self.hitbox.centery

	def jump(self, height):
		self.vel.y = -height

	def physics_x(self, dt):

		self.old_hitbox = self.hitbox.copy()
		
		self.acc.x += self.vel.x * self.fric
		self.vel.x += self.acc.x * dt
		
		#self.pos.x += self.vel.x
		self.pos.x += self.vel.x * dt + (0.5 * self.acc.x) * (dt**2)

		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx

		self.pushable_collisions('x')
		self.collisions('x')
		self.platforms(self.zone.platform_sprites, dt)
		self.platforms(self.zone.pushable_sprites, dt)

		# if player is going slow enough, make the player stand still
		#if abs(self.vel.x) < 0.1: self.vel.x = 0

	def physics_y(self, dt):

		
		
		# Double the gravity if not holding jump key to allow variale jump height
		if not (pygame.key.get_pressed()[pygame.K_UP]) and self.vel.y < 0 and not self.zone.cutscene_running: 
			self.vel.y += (self.acc.y * 2.5) * dt
		else:
			self.vel.y += self.acc.y * dt

		#self.pos.y += self.vel.y
		self.pos.y += self.vel.y * dt + (0.5 * self.acc.x) * (dt**2)
		
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery

		self.collisions('y') 
		self.pushable_collisions('y')
		
		# limit max fall speed
		if self.vel.y >= self.max_fall_speed: 
			self.vel.y = self.max_fall_speed

		# Make the player off ground if moving in y direction
		if abs(self.vel.y) >= 0.5: 
			self.on_ground = False

		self.old_hitbox = self.hitbox.copy()


	def handle_jumping(self, dt):
		# incrememnt cyote timer when not on ground
		if not self.on_ground: 
			self.cyote_timer += dt
		else: 
			self.cyote_timer = 0
		# # if falling, this gives the player one jump if they have double jump
		# if self.jump_counter == 0 and self.cyote_timer < self.cyote_timer_threshold:
		# 	self.jump_counter = 1

		# jump buffer activated if pressing jump in air
		if self.jump_buffer_active:
			self.jump_buffer += dt
			if self.jump_buffer >= self.jump_buffer_threshold:
				self.jump_buffer = 0
				self.jump_buffer_active = False

	def state_logic(self):
		new_state = self.state.state_logic(self)
		if new_state: self.state = new_state
		else: self.state

	def update(self, dt):
		self.state_logic()
		self.state.update(self, dt)
		self.collide_hazards()
		self.handle_jumping(dt)





		


		
		