
from settings import *

class Entity(pygame.sprite.Sprite):
	def __init__(self, game, zone, name, groups, pos, z):
		super().__init__(groups)

		self.game = game
		self.zone = zone
		self.z = z
		self.block_sprites = self.zone.block_sprites
		self.name = name

		self.image = pygame.Surface((20,20))
		#self.image = pygame.image.load(f'../assets/hazards/{self.name}.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(0, 0)
		self.old_hitbox = self.hitbox.copy()

		self.fric = -0.2
		self.acc = pygame.math.Vector2(0, 0)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.old_pos = self.pos.copy()
		self.vel = pygame.math.Vector2()
		self.platform_speed = pygame.math.Vector2()
		self.prev_platform = None

		# player collide type
		self.on_ground = False
		self.max_fall_speed = 7

	def platforms(self, group, dt):
		for platform in group:
			platform_raycast = pygame.Rect(platform.rect.x, platform.rect.y - platform.rect.height * 0.2, platform.rect.width, platform.rect.height)
			if self.hitbox.colliderect(platform.rect) or self.hitbox.colliderect(platform_raycast): 
				if self.hitbox.bottom <= platform.rect.top + 4 and self.vel.y >= 0:
					self.platform_vel = platform.pos - platform.old_pos
					self.hitbox.bottom = platform.rect.top
					self.on_ground = True
					self.vel.y = 0

					self.rect.centery = self.hitbox.centery
					self.pos.y = self.hitbox.centery

					if not hasattr(self, 'prev_platform'):
						self.prev_platform = platform
						self.platform_vel.x = 0
					else:
						self.platform_vel.x = platform.pos.x - platform.old_pos.x
						self.prev_platform = platform

					self.pos.x += self.platform_vel.x

	def physics_x(self, dt):
		self.old_hitbox = self.hitbox.copy()
		self.old_pos = self.pos.copy()

		self.acc.x += self.vel.x * self.fric
		self.vel.x += self.acc.x * dt
		
		self.pos.x += self.vel.x * dt + (0.5 * self.acc.x) * (dt**2)

		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		
		self.collisions('x')
		self.platforms(self.zone.platform_sprites, dt)
		self.platforms(self.zone.pushable_sprites, dt)

	def physics_y(self, dt):

		self.vel.y += self.acc.y * dt

		self.pos.y += self.vel.y * dt + (0.5 * self.acc.y) * dt
		self.hitbox.centery = round(self.pos.y)
		self.collisions('y') 
		self.rect.centery = self.hitbox.centery

		# limit max fall speed
		if self.vel.y >= self.max_fall_speed: 
			self.vel.y = self.max_fall_speed

		# Make the player off ground if moving in y direction
		if abs(self.vel.y) >= 0.5: 
			self.on_ground = False

		# apply gravity always
		self.acc.y = self.zone.gravity

	def update(self, dt):
		self.acc.x = 0
		self.physics_x(dt)
		self.physics_y(dt)

class Box(Entity):
	def __init__(self, game, zone, name, groups, pos, z):
		super().__init__(game, zone, name, groups, pos, z)

		self.image = pygame.image.load(f'../assets/hazards/{self.name}.png').convert_alpha()

	def collisions(self, direction):

		for sprite in self.block_sprites:
			if sprite.hitbox.colliderect(self.hitbox):

				if direction == 'x':
					if self.hitbox.right >= sprite.hitbox.left and self.old_hitbox.right <= sprite.old_hitbox.left:
						self.hitbox.right = sprite.hitbox.left
						self.vel.x *= -1
					
					elif self.hitbox.left <= sprite.hitbox.right and self.old_hitbox.left >= sprite.old_hitbox.right:
						self.hitbox.left = sprite.hitbox.right
						self.vel.x *= -1

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

	def update(self, dt):
		self.acc.x = 0
		self.physics_x(dt)
		self.physics_y(dt)