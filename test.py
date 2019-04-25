#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7

import pygame
import sys
pygame.init()

# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((100, 100))

print(screen.get_size())

IMG = pygame.image.load('block.png')
rect = IMG.get_rect()
oldcenter = rect.center
angle = 0

print(-10.7208178788, round(-10.7208178788))
print(3.58443540759, round(3.58443540759))



while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

	