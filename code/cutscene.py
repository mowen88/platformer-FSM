
from state import State
from settings import *
from dialogue import Dialogue

class Cutscene0(State):
	def __init__(self, game, zone, number):
		State.__init__(self, game)

		self.zone = zone
		self.number = number
		self.opening = True

		self.bar_height = 0
		self.target_height = HEIGHT * 0.1
		self.blackbar = pygame.Surface((WIDTH, self.bar_height))

		self.target = pygame.math.Vector2(self.zone.target.rect.center)
		self.new_pos = pygame.math.Vector2()

		self.timer = 0
		self.int_time = 0


	def create_dialogue(self, target_sprite, dialogue_index, duration):
		Dialogue(self.game, self.zone, self.number, target_sprite, dialogue_index, duration).enter_state()

	def move_camera(self):
		self.target.x += (self.new_pos.x - self.target.x)/200
		self.target.y += (self.new_pos.y - self.target.y)/200
		
	def blackbars(self, screen):
		
		if not self.opening:
		    self.bar_height -= (self.target_height - self.bar_height) / 60

		    if self.bar_height <= 0:
		        self.bar_height = 0
		        self.opening = True
		        self.exit_state()

		elif self.bar_height < self.target_height - 1:  
		    self.bar_height += (self.target_height - self.bar_height) / 60

		pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, self.bar_height))
		pygame.draw.rect(screen, BLACK, (0, HEIGHT - self.bar_height, WIDTH, self.target_height))

	def sequence(self):

		if self.int_time < 60:
			self.target = pygame.math.Vector2(self.zone.target.rect.center)

		# move the camera new position after short cooldown above
		elif self.int_time == 65:
			self.zone.target.jump(6)
			self.zone.target.move['left'] = True
		elif self.int_time == 105:
			self.zone.target.move['left'] = False
			self.create_dialogue(self.zone.npc, 0, 60)
		elif self.int_time < 300:
			self.new_pos = pygame.math.Vector2(self.zone.npc.rect.midtop)
		elif self.int_time == 420:
		 	self.create_dialogue(self.zone.target, 1, 100)
		elif self.int_time < 540:
			self.new_pos = pygame.math.Vector2(self.zone.target.rect.center)

		elif self.int_time > 600:
			self.opening = False
			self.zone.cutscene_running = False

	def update(self, dt):
		self.game.reset_keys()
		self.timer += dt
		self.int_time = int(self.timer)
		self.prev_state.update(dt)


	def render(self, screen):
		self.move_camera()
		self.sequence()
		self.prev_state.rendered_sprites.offset_draw(self.target)

		self.blackbars(screen)

		self.game.render_text(self.zone.target.move, WHITE, self.game.small_font, RES/2)


class Cutscene1(Cutscene0):

	def update(self, dt):
		self.game.reset_keys()
		self.timer += dt
		self.int_time = int(self.timer)
		self.prev_state.update(dt)

	def render(self, screen):

		self.move_camera()
		self.sequence()
		self.prev_state.rendered_sprites.offset_draw(self.target)
		self.blackbars(screen)
