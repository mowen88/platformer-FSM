import pygame
from state import State
from settings import *

class Dialogue(State):
    def __init__(self, game, zone, cutscene_number, sprite, dialog_number, duration):
        super().__init__(game)

        self.game = game
        self.cutscene_number = cutscene_number
        self.sprite = sprite
        self.dialog_number = dialog_number
        self.sprite = sprite
        self.duration = duration
        self.offset = self.sprite.zone.rendered_sprites.offset

        self.opening = True

        self.box_width = 0
        self.center = (self.sprite.rect.centerx - self.offset.x, self.sprite.rect.top - 25 - self.offset.y)
        self.target_width = TILESIZE * 10

        self.lines = DIALOGUE[self.cutscene_number][self.dialog_number]
        self.char_indices = [0] * len(self.lines)

        self.timer = 0

    def opening_box(self, screen):
        if not self.opening:
            self.box_width -= (self.target_width - self.box_width) / 30

            if self.box_width <= 0:
                self.box_width = 0
                self.opening = True
                self.exit_state()

        elif self.box_width < self.target_width - 1:
            self.box_width += (self.target_width - self.box_width) / 45

        if self.timer > self.duration:
            self.opening = False

        else:
            # draw arrow to sprite head
            vertices = [(self.center[0] - 5, self.center[1] + 20), (self.center[0] + 5, self.center[1] + 20), (self.sprite.rect.midtop - self.offset)]
            pygame.draw.polygon(self.game.screen, WHITE, vertices, 0)

        pygame.draw.rect(screen, WHITE, (self.center[0] - self.box_width/2, self.center[1] - 25, self.box_width, 45), border_radius = 8)


    def draw_text(self):
        total_height = len(self.lines) * 10  # Assuming each line has a height of 10 units
        start_y = self.center[1] - total_height // 2
        
        if self.opening:
            for index, line in enumerate(self.lines):
                rendered_line = self.lines[index][:self.char_indices[index]]
                y_position = start_y + 10 * index
                self.game.render_text(rendered_line, BLACK, self.game.small_font, (self.center[0], y_position))

    def update(self, dt):
        self.timer += dt

        if ACTIONS['return']:
            self.exit_state()
        self.game.reset_keys()

        self.prev_state.update(dt)

        if not self.char_indices[-1] >= len(self.lines[-1]):
            if self.timer > 1:
                self.timer = 0

                for i in range(len(self.lines)):
                    self.char_indices[i] += 1
                    if self.char_indices[i] > len(self.lines[i]):
                        self.char_indices[i] = len(self.lines[i])
                    else:
                        break
       

    def render(self, screen):
        self.prev_state.render(screen)

        self.center = (self.sprite.rect.centerx - self.offset.x, self.sprite.rect.top - 25 - self.offset.y)
        self.opening_box(screen)
        self.draw_text()
