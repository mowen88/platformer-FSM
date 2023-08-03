import pygame
from settings import *
from npc_fsm import Fall

class NPC(pygame.sprite.Sprite):
	def __init__(self, game, zone, name, groups, pos, z, block_sprites):
		super().__init__(groups)

		self.game = game
		self.zone = zone
		self.z = z
		self.block_sprites = block_sprites

		# animation
		self.name = name
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
		self.moving_right = False
		self.moving_left = False
		self.angle = 0
		self.target_angle = 0
		self.gravity = 0.3
		self.fric = -0.16
		self.acc = pygame.math.Vector2(0, self.gravity)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.dir = pygame.math.Vector2()
		self.on_platform = False
		self.platform_speed = pygame.math.Vector2()

		# jumping
		self.jump_height = 7
		self.max_fall_speed = 12

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
		self.angle += (-(self.dir.x * 3) - self.angle)/10
		self.image = pygame.transform.rotate(right_image, self.angle)
		self.rect = self.image.get_rect(center = self.rect.center)

	def move(self):
		if self.moving_right:
			self.acc.x += 0.5
			self.target_angle = 10
		elif self.moving_left:
			self.acc.x -= 0.5
			self.target_angle = -10
		else:
			self.moving_right, self.moving_left = False, False
			self.target_angle = 0

		if self.dir.x > 0:
			self.facing = 0
		else:
			self.facing = 1

	def platforms(self, dt):
		for platform in self.zone.platform_sprites:
			platform_raycast = pygame.Rect(platform.rect.x, platform.rect.y - platform.rect.height * 0.2, platform.rect.width, platform.rect.height)
			if self.hitbox.colliderect(platform.rect) or self.hitbox.colliderect(platform_raycast): 
				if self.hitbox.bottom <= platform.rect.top + 4 and self.dir.y >= 0:
					self.on_platform = True	
			else:
				self.on_platform = False

		for platform in self.zone.platform_sprites:
			platform_raycast = pygame.Rect(platform.rect.x, platform.rect.y - platform.rect.height * 0.2, platform.rect.width, platform.rect.height)
			if self.hitbox.colliderect(platform.rect) or self.hitbox.colliderect(platform_raycast): 
				if self.hitbox.bottom <= platform.rect.top + 4 and self.dir.y >= 0:
					self.on_platform = True
					self.platform_speed.x = platform.dir.x
					self.hitbox.bottom = platform.rect.top
					self.on_ground = True
					self.dir.y = 0

					self.rect.centery = self.hitbox.centery
					self.pos.y = self.hitbox.centery

	def collisions(self, direction):

		for sprite in self.block_sprites:
			if sprite.rect.colliderect(self.hitbox):

				if direction == 'x':
					if self.hitbox.right >= sprite.rect.left and self.old_hitbox.right <= sprite.old_rect.left:
						self.hitbox.right = sprite.rect.left
					
					elif self.hitbox.left <= sprite.rect.right and self.old_hitbox.left >= sprite.old_rect.right:
						self.hitbox.left = sprite.rect.right

					self.rect.centerx = self.hitbox.centerx
					self.pos.x = self.hitbox.centerx

				if direction == 'y':
					if self.hitbox.bottom >= sprite.rect.top and self.old_hitbox.bottom <= sprite.old_rect.top:
						self.hitbox.bottom = sprite.rect.top
						self.on_ground = True
						self.dir.y = 0
			
					elif self.hitbox.top <= sprite.rect.bottom and self.old_hitbox.top >= sprite.old_rect.bottom:
						self.hitbox.top = sprite.rect.bottom
						self.on_ceiling = True
						self.dir.y = 0

					self.rect.centery = self.hitbox.centery
					self.pos.y = self.hitbox.centery

	def jump(self, height):
		self.dir.y = -height

	def physics_x(self, dt):

		self.old_hitbox = self.hitbox.copy()

		self.acc.x += self.dir.x * self.fric
		self.dir.x += self.acc.x * dt
		
		if self.on_platform:
			self.pos.x += (self.dir.x + self.platform_speed.x) * dt + (0.5 * self.acc.x) * (dt**2)
		else:
			self.pos.x += self.dir.x * dt + (0.5 * self.acc.x) * (dt**2)

		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		
		self.collisions('x')
		self.platforms(dt)

		# if player is going slow enough, make the player stand still
		#if abs(self.dir.x) < 0.1: self.dir.x = 0

	def physics_y(self, dt):

		self.dir.y += self.acc.y * dt

		self.pos.y += self.dir.y * dt + (0.5 * self.acc.y) * dt
		self.hitbox.centery = round(self.pos.y)
		self.collisions('y') 
		self.rect.centery = self.hitbox.centery

		# limit max fall speed
		if self.dir.y >= self.max_fall_speed: 
			self.dir.y = self.max_fall_speed

		# Make the player off ground if moving in y direction
		if abs(self.dir.y) >= 0.5: 
			self.on_ground = False

	def state_logic(self):
		new_state = self.state.state_logic(self)
		if new_state: self.state = new_state
		else: self.state

	def update(self, dt):
		self.state_logic()
		self.state.update(self, dt)



		


		
		