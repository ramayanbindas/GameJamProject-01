"""About the file"""
import pygame

vec = pygame.math.Vector2
class UpWordObsticle(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.pos = vec(x, y)
		self.width, self.height = (100, 30)
		self.image = pygame.Surface((self.width, self.height))
		self.image.fill(pygame.Color("Green"))
		self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

	def update(self, *args):
		pass

	def blit(self, display, delta_time):
		self.update(*[delta_time])
		display.blit(self.image, self.rect)