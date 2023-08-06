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

		self.zone = zone
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)	
		self.z = z
		self.hitbox = self.rect.copy().inflate(0,0)	
		self.old_hitbox = self.hitbox.copy()
		self.pos = pygame.math.Vector2(self.rect.topleft)

class AnimatedTile(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, surf, z = LAYERS['blocks']):
		super().__init__(groups)

		self.game = game
		self.z = z
		self.frames = self.game.get_folder_images(surf)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		
	def animate(self, animation_speed):
		self.frame_index += animation_speed
		self.frame_index = self.frame_index % len(self.frames)
		self.image = self.frames[int(self.frame_index)]

	def update(self, dt):
		self.animate(0.2 * dt)

class DisappearingPlatform(AnimatedTile):
	def __init__(self, game, zone, groups, pos, surf, z = LAYERS['blocks']):
		super().__init__(game, zone, groups, pos, surf, z)

		self.zone = zone
		self.frames = self.game.get_folder_images(surf)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
		self.pos = pygame.math.Vector2(self.rect.topleft)

		self.something_on_platform = False
		self.crumbling = False
		self.timer = 0
		# frame in folder on which the platform stays on before touched
		self.stable_frame = 6

		# get white mask to flash platform when it returns
		self.mask = pygame.mask.from_surface(self.frames[0])
		self.mask_image = self.mask.to_surface()
		self.mask_image.set_colorkey((0, 0, 0))

	def get_player_on_platform(self, dt):
		# taken from character class, where we need to set the timer and platform to this specific platform
		platform_raycast = pygame.Rect(self.rect.x, self.rect.y - self.rect.height * 0.2, self.rect.width, self.rect.height)
		if self.zone.target.hitbox.colliderect(self.rect) or self.zone.target.hitbox.colliderect(platform_raycast): 
			if self.zone.target.hitbox.bottom <= self.rect.top + 4 and self.zone.target.vel.y >= 0 and self.timer == 0:
				self.something_on_platform = True
			else:
				self.something_on_platform = False

	def animation_logic(self, dt):
		if self.timer == 0:
			# increment flashing frames to show when platform returns
			self.frame_index += 0.5 * dt
			if self.frame_index >= self.stable_frame:
				self.frame_index = self.stable_frame
				# once on stable frame, if the player lands on the platform, set to crumbling
				if self.something_on_platform:
					self.crumbling = True

		if self.crumbling:
			self.timer += dt
			self.frame_index += 0.5 * dt
			if self.frame_index >= len(self.frames):
				self.frame_index = len(self.frames)-1
				self.zone.platform_sprites.remove(self)
				if self.timer > 200:
					self.zone.platform_sprites.add(self)
					self.crumbling = False
					self.timer = 0
					self.frame_index = 0

		self.image = self.frames[int(self.frame_index)]

	def update(self, dt):
		self.old_pos = self.pos.copy()
		self.get_player_on_platform(dt)
		self.animation_logic(dt)

		print(self.timer)

class EscalatorPlatform(AnimatedTile):
	def __init__(self, game, zone, groups, pos, surf, direction, amplitude, z = LAYERS['particles']):
		super().__init__(game, zone, groups, pos, surf, z)

		self.zone = zone
		self.direction = pygame.math.Vector2(direction)
		self.vel = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.topleft)
		
	def update(self, dt):
		self.old_pos = self.pos.copy()
		self.pos.x += self.direction.x * dt
		self.animate((self.direction.x/4) * dt)

class MovingPlatform(Tile):
	def __init__(self, game, zone, groups, pos, surf, direction, amplitude, z = LAYERS['particles']):
		super().__init__(game, zone, groups, pos, surf, z)
		
		self.direction = pygame.math.Vector2(direction)
		self.vel = pygame.math.Vector2()
		self.start_pos = pygame.math.Vector2(self.rect.center)
		self.amplitude = amplitude

	def move(self, dt):
		# Update the position using a sine wave pattern
		self.vel += self.direction * dt
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



