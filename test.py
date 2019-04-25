#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7

import pygame
import sys
import math
import random
pygame.init()

# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((100, 100))


print(random.randint(0, 1))
print(random.randint(0, 1))
print(random.randint(0, 1))
print(random.randint(0, 1))
print(random.randint(0, 1))
print(random.randint(0, 1))
print(random.randint(0, 1))



while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

	