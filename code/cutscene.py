from state import State
from settings import *


class Cutscene(State):
	def __init__(self, game, zone):
		State.__init__(self, game)

		self.zone = zone

		self.speed = 30
		self.opening = True

		self.bar_height = 0
		self.target_height = HEIGHT * 0.1
		self.blackbar = pygame.Surface((WIDTH, self.bar_height))

	def blackbars(self):
		
		if not self.opening:
		    self.bar_height -= (self.target_height - self.bar_height) / self.speed

		    if self.bar_height <= 0:
		        self.bar_height = 0
		        self.opening = True
		        self.exit_state()

		elif self.bar_height < self.target_height - 1:  
		    self.bar_height += (self.target_height - self.bar_height) / self.speed


	def update(self, dt):

		if ACTIONS['return']: 
			self.opening = False
		self.game.reset_keys()

		self.blackbars()

		self.prev_state.update(dt)

		


	def render(self, screen):
		self.prev_state.render(screen)
		pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, self.bar_height))
		pygame.draw.rect(screen, BLACK, (0, HEIGHT - self.bar_height, WIDTH, self.target_height))

		print(self.bar_height)
		