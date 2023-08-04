
from settings import *

class Dialogue():
	def __init__(self, game, zone, sprite, cutscene_number):

		self.sprite = sprite
		self.cutscene_number = cutscene_number
		self.offset = self.sprite.zone.rendered_sprites.offset

		self.dialogue_dict = DIALOGUE[self.cutscene_number]
		
		self.active = True

		print(self.dialogue_dict)

	def stop(self):
		self.game.reset_keys()
		self.exit_state()

	def update(self, dt):

		if ACTIONS['return']: 
			self.exit_state()
		self.game.reset_keys()

		# self.prev_state.update(dt)

		# if not self.active:
		# 	self.exit_state()

	def render(self, screen):
		# self.prev_state.render(screen)
		pygame.draw.rect(screen, PINK, (self.sprite.rect.left - 75 - self.offset.x, self.sprite.rect.top - 75 - self.offset.y, 100, 50))