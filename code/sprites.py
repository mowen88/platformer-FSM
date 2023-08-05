import pygame, math
from settings import *

class CutsceneCollider(pygame.sprite.Sprite):
	def __init__(self, groups, rect, number):
		super().__init__(groups)

		self.number = int(number)
		#self.image = pygame.Surface((size))
		self.rect = pygame.Rect(rect)

class Tile(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, surf, z = LAYERS['blocks']):
		super().__init__(groups)

		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)	
		self.z = z	
		self.old_rect = self.rect.copy()

class Platform(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, surf, direction, z = LAYERS['particles']):
		super().__init__(groups)

		self.zone = zone
		self.velection = pygame.math.Vector2(direction)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)	
		self.z = z
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.vel = pygame.math.Vector2(self.velection)

		self.start_pos = pygame.math.Vector2(self.rect.center)
		
	def update(self, dt):

		self.pos += self.vel * dt

class CircularPlatform(Platform):
	def __init__(self, game, zone, groups, pos, surf, direction, z = LAYERS['particles']):
		super().__init__(game, zone, groups, pos, surf, direction, z)

	def update(self, dt):

		if self.rect.centery < self.start_pos.y:
			self.vel.y += 0.05 * dt
		else:
			self.vel.y -= 0.05 * dt

		if self.vel.y >= 0.01:
			self.vel.x += 0.05 * dt
		else:
			self.vel.x -= 0.05 * dt

		self.pos += self.vel * dt
		self.rect.topleft = round(self.pos)


class MovingPlatform(Platform):
	def __init__(self, game, zone, groups, pos, surf, direction, amplitude, z = LAYERS['particles']):
		super().__init__(game, zone, groups, pos, surf, direction, z)
		
		self.amplitude = amplitude
		self.vel = pygame.math.Vector2()

	def move(self, dt):
		# Update the position using a sine wave pattern
		self.vel += self.velection * dt
		self.pos.x = self.start_pos.x + self.amplitude * math.sin(self.vel.x * 0.1)
		self.pos.y = self.start_pos.y + self.amplitude * math.sin(self.vel.y * 0.1)
		self.rect.center = round(self.pos)

	def update(self, dt):
		#get pos before it is updated to get the displacement of movement per frame and pass it to the player platform_speed
		self.old_pos = self.pos.copy()
		self.move(dt)


class SawBlade(MovingPlatform):
	def __init__(self, game, zone, groups, pos, surf, direction, amplitude, z = LAYERS['particles']):
		super().__init__(game, zone, groups, pos, surf, direction, amplitude, z)

		self.angle = 0
		self.original_image = surf
		self.image = surf
		self.speed = 20

	def rotate(self, dt):
		# self.angle += (self.pos.x - self.old_pos.x) * 50 * dt
		self.angle += - 10 * dt
		self.image = pygame.transform.rotate(self.original_image, self.angle)
		self.rect = self.image.get_rect(center = self.pos)

	def update(self, dt):
		self.old_pos = self.pos.copy()
		self.move(dt)
		self.rotate(dt)

# disappearing platform
# timed platform with activator
# moving crates
# escalator platform xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# bouncing thing
# breakable wall

# spikes
# arrows
# fire pits
# fire walls



