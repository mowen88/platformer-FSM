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
        self.target_width = WIDTH * 0.4
        self.box = pygame.Rect(0, 0, 0, 0)

        self.lines = DIALOGUE[self.cutscene_number]
        self.line_char_indices = [0] * len(self.lines)

        self.timer = 0

    def opening_box(self, screen):
        if not self.opening:
            self.box_width -= (self.target_width - self.box_width) / 30

            if self.box_width <= 0:
                self.box_width = 0
                self.opening = True
                self.exit_state()

        elif self.box_width < self.target_width - 1:
            self.box_width += (self.target_width - self.box_width) / 30

        if self.timer > self.duration:
            self.opening = False

        total_lines_height = len(self.lines) * 10  # Assuming height is 10 per line
        self.box = pygame.draw.rect(screen, BLACK, (self.center[0] - self.box_width / 2, self.center[1] - total_lines_height / 2, self.box_width, total_lines_height), border_radius=5)

    def draw_text(self):
        line_height = 10
        for i, line in enumerate(self.lines):
            char_index = self.line_char_indices[i]
            display_line = line[:char_index]
            line_y = self.box.center[1] - (len(self.lines) * line_height) / 2 + i * line_height
            self.game.render_text(display_line, WHITE, self.game.small_font, (self.box.center[0], line_y))

    def update(self, dt):
        self.timer += dt

        if ACTIONS['return']:
            self.exit_state()
        self.game.reset_keys()

        self.prev_state.update(dt)

        if self.timer > 4:
            self.timer = 0
            for i in range(len(self.lines)):
                self.line_char_indices[i] += 1
                if self.line_char_indices[i] > len(self.lines[i]):
                    self.line_char_indices[i] = len(self.lines[i])

    def render(self, screen):
        self.prev_state.render(screen)
        self.center = (self.sprite.rect.centerx - self.offset.x, self.sprite.rect.top - 25 - self.offset.y)
        self.opening_box(screen)
        self.draw_text()
