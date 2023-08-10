import pygame, math, random
from settings import *

class Camera(pygame.sprite.Group):
    def __init__(self, game, zone):
        super().__init__()

        self.game = game
        self.zone = zone
        self.offset = pygame.math.Vector2()
        self.acc = pygame.math.Vector2()
        self.screenshake_timer = 0

        # fog variables
        self.dark = True
        self.main_fog = self.get_fog_image(PINK, (self.zone.size), self.zone.size)

    def get_fog_image(self, colour, circle_size, canvas_size):
        self.fog_colour = colour
        self.fog_surf = pygame.Surface((canvas_size))
        self.light_mask = pygame.image.load(f'../zones/{self.zone.name}/bg_images/2x6_white.png').convert_alpha()
        self.light_mask = pygame.transform.scale(self.light_mask, (circle_size))
        self.light_rect = self.light_mask.get_rect()
        
    def render_fog(self, screen, target):
        self.fog_surf.fill(self.fog_colour)
        self.light_rect.center = target
        self.fog_surf.blit(self.light_mask, self.light_rect)
        screen.blit(self.fog_surf, (0,0), special_flags = pygame.BLEND_MULT)

    def screenshake(self):
        if self.game.screenshaking:
            self.screenshake_timer += 1
            if self.screenshake_timer < 120:
                random_number = random.randint(-1, 1)
                self.offset += [random_number, random_number]
            else:
                self.game.screenshaking = False

    def screenshake_update(self, dt):
        self.screenshake_timer *= dt

    def zone_limits(self):
        if self.offset[0] <= 0: self.offset[0] = 0
        elif self.offset[0] >= self.zone.size[0] - WIDTH: self.offset[0] = self.zone.size[0] - WIDTH
        if self.offset[1] <= 0: self.offset[1] = 0
        elif self.offset[1] >= self.zone.size[1] - HEIGHT: self.offset[1] = self.zone.size[1] - HEIGHT

    def offset_draw(self, screen, target):
        screen.fill(LIGHT_GREY)  

        #mouse_dist = self.zone.get_distance(pygame.mouse.get_pos(), target.rect.center) / 10

        self.offset += (target - RES/2 - self.offset)

        # limit offset to stop at edges
        self.zone_limits()
        # Apply screenshake effect if needed
        self.screenshake()

        # # dark mode
        # if self.dark:
        #     self.render_fog(screen, (0 - self.offset[0] * 0.1, 0 - self.offset[1] * 0.1))

        for layer in LAYERS.values():
            for sprite in self.zone.rendered_sprites:
                if sprite.z == layer:
                    offset = sprite.rect.topleft - self.offset
                    screen.blit(sprite.image, offset)

        
