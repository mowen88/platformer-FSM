
from state import State
from settings import *
from dialogue import Dialogue

class Cutscene(State):
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

	def move_camera(self, dt):
		self.target.x += (self.new_pos.x - self.target.x) * 0.05 * dt
		self.target.y += (self.new_pos.y - self.target.y) * 0.05 * dt
		
	def blackbar_logic(self, dt):
		if not self.opening:
		    self.bar_height -= (self.target_height - self.bar_height) * 0.1 * dt

		    if self.bar_height <= 0:
		        self.bar_height = 0
		        self.opening = True
		        self.zone.cutscene_running = False
		        self.exit_state()

		elif self.bar_height < self.target_height - 1:  
		    self.bar_height += (self.target_height - self.bar_height) * 0.1 * dt

	def draw_blackbars(self, screen):
		pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, self.bar_height))
		pygame.draw.rect(screen, BLACK, (0, HEIGHT - self.bar_height, WIDTH, self.target_height))

	def sequence(self):
		if self.number == 0:

			if self.int_time < 60:
				self.target = pygame.math.Vector2(self.zone.target.rect.center)

			# move the camera new position after short cooldown above
			elif self.int_time == 65:
				self.zone.target.jump(6)
				self.zone.npc.move['left'] = True
				self.zone.target.move['left'] = True
			elif self.int_time == 75:
				self.zone.npc.move['left'] = False
			elif self.int_time == 105:
				self.zone.target.move['left'] = False
				self.create_dialogue(self.zone.npc, 0, 60)
			elif self.int_time < 300:
				self.zone.npc.move['left'] = True
				self.new_pos = pygame.math.Vector2(self.zone.npc.rect.midtop)
			elif self.int_time < 360:
				self.zone.npc.move['left'] = False
			elif self.int_time == 420:
				self.create_dialogue(self.zone.target, 1, 100)
			elif self.int_time < 540:
				self.new_pos = pygame.math.Vector2(self.zone.target.rect.center)

			elif self.int_time > 660:
				self.opening = False

		elif self.number == 1:
			if self.int_time < 60:
				self.target = pygame.math.Vector2(self.zone.target.rect.center)

			# move the camera new position after short cooldown above
			elif self.int_time == 105:
				self.create_dialogue(self.zone.npc, 0, 60)
			elif self.int_time < 300:
				self.new_pos = pygame.math.Vector2(self.zone.npc.rect.midtop)
			elif self.int_time == 420:
				self.create_dialogue(self.zone.target, 1, 100)
			elif self.int_time < 540:
				self.new_pos = pygame.math.Vector2(self.zone.target.rect.center)

			elif self.int_time > 600:
				self.opening = False

		elif self.number == 2:
			if self.int_time < 600:
				self.target = pygame.math.Vector2(self.zone.target.rect.center)
			if self.int_time == 130:
				self.create_dialogue(self.zone.target, 0, 100)
			if self.int_time == 400:
				self.create_dialogue(self.zone.target, 1, 100)
			
			if 600 < self.int_time < 700:
				#self.new_pos = pygame.math.Vector2(self.zone.target.rect.center)
				self.zone.target.move['right'] = True
			if self.int_time < 750:
				self.new_pos = pygame.math.Vector2(self.zone.target.rect.center)

			if self.int_time > 900:
				self.opening = False
				

	def update(self, dt):
		self.game.reset_keys()
		self.timer += dt
		self.int_time = int(self.timer)
		self.prev_state.update(dt)

		self.move_camera(dt)
		self.blackbar_logic(dt)

		print(self.opening)

	def render(self, screen):
		
		self.sequence()
		self.prev_state.rendered_sprites.offset_draw(screen, self.target)

		self.draw_blackbars(screen)
		self.game.render_text(COMPLETED_DATA['cutscenes'], WHITE, self.game.small_font, RES/2)


