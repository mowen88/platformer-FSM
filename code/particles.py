import pygame
from settings import *



class GunFlash(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, surf, z = LAYERS['blocks']):
		super().__init__(groups)

		self.zone = zone
		self.image = surf
		self.rect = self.image.get_rect(center = pos)	
		self.z = z

	def show(self, screen, pos = (0,0)):
		self.image.blit(screen, pos)
