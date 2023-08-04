from state import State
from settings import *

class Dialogue(State):
	def __init__(self, game, zone, sprite, cutscene_number, duration):
		State.__init__(self, game)

		self.game = game
		self.sprite = sprite
		self.cutscene_number = cutscene_number
		self.duration = duration
		self.offset = self.sprite.zone.rendered_sprites.offset

		self.dialogue_dict = DIALOGUE[self.cutscene_number]
		
		self.opening = True

		self.box_width = 0
		self.center = (self.sprite.rect.centerx - self.offset.x, self.sprite.rect.top - 25 - self.offset.y)
		self.target_width = WIDTH * 0.5
		self.box = pygame.Surface((WIDTH, self.box_width))


		self.current_char_index = 0
		self.current_dialogue = DIALOGUE[self.cutscene_number]

		self.timer = 0


	def opening_box(self, screen):
		if not self.opening:
		    self.box_width -= (self.target_width - self.box_width) / 10

		    if self.box_width <= 0:
		        self.box_width = 0
		        self.opening = True
		        self.exit_state()

		elif self.box_width < self.target_width - 1:  
		    self.box_width += (self.target_width - self.box_width) / 10

		if self.timer > self.duration:
			self.opening = False

		pygame.draw.rect(screen, BLACK, (self.center[0] - self.box_width/2, self.center[1] - 30, self.box_width, 60))

	def draw_text(self):
		text_to_display = self.current_dialogue[:self.current_char_index]  # Get characters up to current_char_index
		self.game.render_text(text_to_display, WHITE, self.game.small_font, self.center)

	def update(self, dt):
		self.timer += dt

		if ACTIONS['return']: 
			self.exit_state()
		self.game.reset_keys()

		self.prev_state.update(dt)

		if self.timer > 5:
			self.timer = 0
			self.current_char_index += 1
			if self.current_char_index > len(self.current_dialogue):
				self.current_char_index = len(self.current_dialogue)

		print(self.timer)

	def render(self, screen):
		self.prev_state.render(screen)
		rect = pygame.Rect(self.sprite.rect.left - 75 - self.offset.x, self.sprite.rect.top - 55 - self.offset.y, 100, 50)

		self.center = (self.sprite.rect.centerx - self.offset.x, self.sprite.rect.top - 35 - self.offset.y)
		#pygame.draw.rect(screen, LIGHT_GREEN, rect, border_radius=5)
		self.opening_box(screen)

		# if self.box_width >= self.target_width -1:
		# 	self.game.render_text(self.dialogue_dict, WHITE, self.game.small_font, self.center)

		self.draw_text()	
