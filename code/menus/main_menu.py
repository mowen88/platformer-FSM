
from state import State
from zone import Zone
from entities.npc import NPC
from settings import *

class MainMenu(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.game = game
		self.state = 'Start'
		self.alpha = 0
		
	def fadein(self, dt):
		self.alpha += 5 * dt
		if self.alpha >= 255:
			self.alpha = 255

		surf.fill(colour)
		surf.set_alpha(alpha)
		rect = surf.get_rect(center = RES/2)
		return(surf, rect)

	def render_button(self, screen, state, text_colour, button_colour, hover_colour, pos):

		mx, my = pygame.mouse.get_pos()

		colour = text_colour
		#surf.fill(button_colour)
		#surf.set_alpha(self.alpha)
		surf = self.game.small_font.render(str(state), False, colour)
		rect = surf.get_rect(center = pos).inflate(30,10)
		#screen.blit(surf, rect)

		if rect.collidepoint(mx, my):
			pygame.draw.rect(screen, hover_colour, rect, border_radius=8)#int(HEIGHT * 0.05))
			self.game.render_text(state, button_colour, self.game.small_font, pos)
		else:
			pygame.draw.rect(screen, button_colour, rect, border_radius=8)#int(HEIGHT * 0.05))
			self.game.render_text(state, text_colour, self.game.small_font, pos)

			# if pygame.mouse.get_pressed()[0] == 1 and not self.fading_out:
			# 	self.state = state
			# 	self.fading_out = True


		# if self.alpha >= 255:
		# 	if rect.collidepoint(mx, my) or self.state == state:
		# 		pygame.draw.rect(self.game.screen, hover_colour, rect)
		# 		self.game.render_text(state, button_colour, self.game.smaller_font, pos)
		# 		if pygame.mouse.get_pressed()[0] == 1 and not self.fading_out:
		# 			self.state = state
		# 			self.fading_out = True


	def update(self, dt):

		if ACTIONS['return']: 
			Zone(self.game, PLAYER_DATA['current_zone'], PLAYER_DATA['entry_pos']).enter_state()
		self.game.reset_keys()

	def render(self, screen):
		screen.fill(RED)

		self.render_button(screen, self.state, YELLOW, BLACK, YELLOW, RES/2)

	# def update(self):
		
	# 	self.fadein()
	# 	if self.fading_out:
	# 		self.fadeout_alpha += 255//50
	# 		if self.fadeout_alpha >= 255:
	# 			if self.state == 'Race':
	# 				self.selections_menu.enter_state()
	# 			if self.state == 'Leaderboard':
	# 				Leaderboard(self.game, self.level, self.game.car_type, 'Menu').enter_state()
	# 			if self.state == 'Controls':
	# 				Controls(self.game).enter_state()
	# 			if self.state == 'Quit':
	# 				self.game.running = False
	# 				self.game.playing = False

	# def render(self, display):
	# 	display.blit(self.background[0], self.background[1])

	# 	self.game.render_text('Main Menu', WHITE, self.game.bigger_font, (HALF_WIDTH, HEIGHT /4))

	# 	self.render_button('Race', WHITE, BLACK, WHITE, (HALF_WIDTH, HEIGHT * 0.4))
	# 	self.render_button('Leaderboard', WHITE, BLACK, WHITE, (HALF_WIDTH, HEIGHT * 0.5))
	# 	self.render_button('Controls', WHITE, BLACK, WHITE, (HALF_WIDTH, HEIGHT * 0.6))
	# 	self.render_button('Quit', WHITE, BLACK, WHITE, (HALF_WIDTH, HEIGHT * 0.7))

	# 	display.blit(self.fade[0], self.fade[1])
	# 	self.fade[0].set_alpha(self.fadeout_alpha)


