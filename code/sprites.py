import pygame, math
from settings import *

class FadeSurf(pygame.sprite.Sprite):
	def __init__(self, zone, groups, pos, alpha = 255, z = LAYERS['foreground']):
		super().__init__(groups)

		self.zone = zone
		self.image = pygame.Surface((self.zone.size))
		self.alpha = alpha
		self.z = z
		self.rect = self.image.get_rect(topleft = pos)

	def update(self, dt):
		if self.zone.exiting:
			self.alpha += 5 * dt
			if self.alpha >= 255: 
				self.alpha = 255
				self.zone.exit_state()
				self.zone.restart_zone(self.zone.new_zone)
			
		elif self.zone.entering:
			self.alpha -= 5 * dt
			if self.alpha <= 0:
				self.alpha = 0
				self.zone.entering = False

	def draw(self, screen):
		self.image.set_alpha(self.alpha)
		screen.blit(self.image, (0,0))

class Collider(pygame.sprite.Sprite):
	def __init__(self, groups, rect):
		super().__init__(groups)

		#self.image = pygame.Surface((size))
		self.rect = pygame.Rect(rect)
		
		self.hitbox = self.rect.copy().inflate(0,0)	
		self.old_hitbox = self.hitbox.copy()

class CutsceneCollider(Collider):
	def __init__(self, groups, rect, number):
		super().__init__(groups, rect)

		self.number = int(number)
		
class Tile(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, surf, z = LAYERS['blocks']):
		super().__init__(groups)

		self.zone = zone
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)	
		self.z = z
		self.hitbox = self.rect.copy()
		self.old_hitbox = self.hitbox.copy()
		self.pos = pygame.math.Vector2(self.rect.topleft)

class BG(Tile):
	def __init__(self, game, zone, groups, pos, surf, parralax_value, z = LAYERS['BG0']):
		super().__init__(game, zone, groups, pos, surf, z)

		self.zone = zone
		self.image = surf
		self.parralax_value = pygame.math.Vector2(parralax_value)
		self.offset = self.zone.rendered_sprites.offset
		self.rect = self.image.get_rect(topleft = pos)	
		self.z = z
		self.hitbox = self.rect.copy().inflate(0,0)	
		self.old_hitbox = self.hitbox.copy()
		self.pos = pygame.math.Vector2(self.rect.topleft)

	def update(self, dt):
		self.rect.topleft = (0 - self.offset[0] * self.parralax_value.x, 0 - self.offset[1] * self.parralax_value.y)

class AnimatedTile(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, surf, z = LAYERS['blocks']):
		super().__init__(groups)

		self.game = game
		self.z = z
		self.frames = self.game.get_folder_images(surf)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(0,0)	
		self.old_hitbox = self.hitbox.copy()
		self.pos = pygame.math.Vector2(self.rect.topleft)
		
	def animate(self, animation_speed):
		self.frame_index += animation_speed
		self.frame_index = self.frame_index % len(self.frames)
		self.image = self.frames[int(self.frame_index)]

	def update(self, dt):
		self.animate(0.2 * dt)
		self.hitbox.center = self.rect.center

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
		self.hitbox.center = self.rect.center

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
		self.animate((self.pos.x - self.old_pos.x) * dt)
		self.hitbox.center = self.rect.center

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
		self.rect.centerx = round(self.pos.x)
		self.rect.centery = round(self.pos.y)

	def update(self, dt):
		#get pos before it is updated to get the displacement of movement per frame and pass it to the player platform_speed
		self.old_pos = self.pos.copy()
		self.move(dt)
		self.hitbox.center = self.rect.center


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
		self.hitbox.center = self.rect.center

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



