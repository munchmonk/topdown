#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7

import pygame
import sys
import math
import random
# pygame.init()

# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((100, 100))


def point_in_blocks(x, y):
	if (x in (2, 3, 4, 5)) or (x in (7, 8, 9)):
		return True
	return False


def get_wall(x, y, wall=[]):
	if not point_in_blocks(x, y):
		return
	if (x, y) in wall:
		return
	wall.append((x, y))
	get_wall(x - 1, y, wall)
	get_wall(x + 1, y, wall)
	return wall

print('#1', get_wall(3, 0, []))
print('#2', get_wall(7, 0, []))


"""
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
"""