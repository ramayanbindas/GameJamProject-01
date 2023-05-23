"""Introduction of the game"""

import pygame
from sys import exit

# Importing in-built modules
from LEVELS.Component.player import SpiderMan
from LEVELS.Component.obsticle import UpWordObsticle

def main() -> None:
	"""Document"""
	pygame.init()

	# Ready the game-main-loop
	screen = pygame.display.set_mode((1200, 700))
	pygame.display.set_caption("Name of the Game")
	clock = pygame.time.Clock()
	FPS = 30
	delta_time = 0
	running = True

	# Initialize all the in-built module staff
	spiderman = SpiderMan((640//2, 480//2),)
	obsticle_group = pygame.sprite.Group()
	obsticle = UpWordObsticle(640//2, 480//2 + 34)
	obsticle_group.add(obsticle)

	while running:
		# fill the screen
		screen.fill(pygame.Color("Black"))

		# pygame event poll
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		# Bliting Objects
		# screen.blit(spiderman.image, spiderman.rect)
		spiderman.blit(screen, delta_time)
		# obsticle_group.draw(screen)
		# obsticle_group.update(*[delta_time])

		# Updating the screen
		pygame.display.update()
		delta_time = clock.tick(FPS)/1000.0 # limits FPS


	# Quiting the game
	pygame.quit()
	exit()

if __name__ == '__main__':
	main()