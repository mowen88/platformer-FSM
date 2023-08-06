import pygame
from settings import *
from player_fsm import Fall

class Player(pygame.sprite.Sprite):
	def __init__(self, game, zone, name, groups, pos, z, block_sprites, pushable_sprites):
		super().__init__(groups)

		self.game = game
		self.zone = zone
		self.z = z
		self.block_sprites = block_sprites
		self.pushable_sprites = pushable_sprites

		# animation
		self.name = 'player'
		self.animations = {'idle':[], 'run':[], 'skid':[], 'land':[], 'jump':[], 'double_jump':[], 'fall':[]}
		self.animation_type = ''
		self.import_images(self.animations)
		self.state = Fall(self)
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
		self.move = {'right':True, 'left':False}
		self.angle = 0
		self.target_angle = 0
		self.gravity = 0.3
		self.fric = -0.2
		self.acc = pygame.math.Vector2(0, self.gravity)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.vel = pygame.math.Vector2()
		self.on_platform = False
		self.platform_speed = pygame.math.Vector2()

		# jumping
		self.jump_height = 7
		self.max_fall_speed = 7
		self.jump_counter = 0
		self.cyote_timer = 0
		self.cyote_timer_threshold = 6
		self.jump_buffer_active = False
		self.jump_buffer = 0
		self.jump_buffer_threshold = 6

		# player collide type
		self.on_ground = False

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
			self.acc.x += 0.5
			self.target_angle = 10
		elif self.move['left']:
			self.acc.x -= 0.5
			self.target_angle = -10
		else:
			self.move['right'], self.move['left'] = False, False 
			self.target_angle = 0

		if self.vel.x > 0:
			self.facing = 0
		else:
			self.facing = 1

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.move['right'] = True
			self.move['left'] = False
		elif keys[pygame.K_LEFT]:
			self.move['left'] = True
			self.move['right'] = False
		else:
			self.move['right'] = False
			self.move['left'] = False

	def platforms(self, dt):
		for platform in self.zone.platform_sprites:
			platform_raycast = pygame.Rect(platform.rect.x, platform.rect.y - platform.rect.height * 0.2, platform.rect.width, platform.rect.height)
			if self.hitbox.colliderect(platform.rect) or self.hitbox.colliderect(platform_raycast): 
				if self.hitbox.bottom <= platform.rect.top + 4 and self.vel.y >= 0:
					self.on_platform = True	
					self.pos.x += self.platform_speed.x
			else:
				self.on_platform = False

		for platform in self.zone.platform_sprites:
			platform_raycast = pygame.Rect(platform.rect.x, platform.rect.y - platform.rect.height * 0.2, platform.rect.width, platform.rect.height)
			if self.hitbox.colliderect(platform.rect) or self.hitbox.colliderect(platform_raycast): 
				if self.hitbox.bottom <= platform.rect.top + 4 and self.vel.y >= 0:
					self.on_platform = True
					self.platform_speed.x = platform.pos.x - platform.old_pos.x
					self.hitbox.bottom = platform.rect.top
					self.on_ground = True
					self.vel.y = 0

					self.rect.centery = self.hitbox.centery
					self.pos.y = self.hitbox.centery

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

		for sprite in self.pushable_sprites:
			if sprite.hitbox.colliderect(self.hitbox):

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
						self.vel.y = 0
			
					elif self.hitbox.top <= sprite.hitbox.bottom and self.old_hitbox.top >= sprite.old_hitbox.bottom:
						self.hitbox.top = sprite.hitbox.bottom
						self.vel.y = 0

					self.rect.centery = self.hitbox.centery
					self.pos.y = self.hitbox.centery


				# if direction == 'y':
				# 	if self.hitbox.bottom >= sprite.rect.top and self.old_hitbox.bottom <= sprite.old_rect.top:
				# 		self.hitbox.bottom = sprite.rect.top
				# 		self.on_ground = True
				# 		self.vel.y = 0
			
				# 	elif self.hitbox.top <= sprite.rect.bottom and self.old_hitbox.top >= sprite.old_rect.bottom:
				# 		self.hitbox.top = sprite.rect.bottom
				# 		self.on_ceiling = True
				# 		self.vel.y = 0

				# 	self.rect.centery = self.hitbox.centery
				# 	self.pos.y = self.hitbox.centery

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
		self.pushable_collisions('x')
		self.platforms(dt)

		# if player is going slow enough, make the player stand still
		#if abs(self.vel.x) < 0.1: self.vel.x = 0

	def physics_y(self, dt):

		# Double the gravity if not holding jump key to allow variale jump height
		if not (pygame.key.get_pressed()[pygame.K_UP]) and self.vel.y < 0 and not self.zone.cutscene_running: 
			self.vel.y += (self.acc.y * 2.5) * dt
		else:
			self.vel.y += self.acc.y * dt

		self.pos.y += self.vel.y * dt + (0.5 * self.acc.y) * dt
		self.hitbox.centery = round(self.pos.y)
		self.collisions('y') 
		self.pushable_collisions('y')
		self.rect.centery = self.hitbox.centery

		# limit max fall speed
		if self.vel.y >= self.max_fall_speed: 
			self.vel.y = self.max_fall_speed

		# Make the player off ground if moving in y direction
		if abs(self.vel.y) >= 0.5: 
			self.on_ground = False

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
		self.handle_jumping(dt)



		


		
		