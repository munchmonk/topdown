#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7

import pygame
import sys
import math


class Camera:
	def __init__(self, game):
		self.game = game
		self.screenwidth, self.screenheight = game.screen.get_size()
		self.maxwidth, self.maxheight = game.maxwidth, game.maxheight
		self.x = 0
		self.y = 0

	def update(self, target):
		self.x = max(0, target.rect.centerx - self.screenwidth // 2)
		self.y = max(0, target.rect.centery - self.screenheight // 2)
		self.x = min(self.x, self.maxwidth - self.screenwidth)
		self.y = min(self.y, self.maxheight - self.screenheight)

	def apply(self, obj):
		obj_rect = obj.rect
		if obj in self.game.allplayers:
			new_rect = pygame.Rect(obj_rect.x - self.x, obj_rect.y - self.y, obj_rect.width, obj_rect.height)
		return pygame.Rect(obj_rect.x - self.x, obj_rect.y - self.y, obj_rect.width, obj_rect.height)



class Zombie(pygame.sprite.Sprite):
	IMG = pygame.image.load('zombie.png')
	SPEED = 0.1

	def __init__(self, game, x, y):
		self.game = game
		self.groups = game.allsprites, game.allzombies
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.image = Zombie.IMG
		self.rect = self.image.get_rect(topleft=(x, y))

		self.angle = 0

	def get_player_coord(self):
		player = self.game.find_player(0)
		return player.rect.centerx, player.rect.centery

	def get_dxdy(self):
		dx, dy = 0, 0
		p_coord = self.get_player_coord()
		delta_x = p_coord[0] - self.rect.centerx
		delta_y = p_coord[1] - self.rect.centery

		if delta_x:
			dx = int(abs(delta_x) / delta_x)
		if delta_y:
			dy = int(abs(delta_y) / delta_y)

		hyp = math.sqrt(delta_x ** 2 + delta_y ** 2)
		if hyp:
			dx = delta_x / hyp
			dy = delta_y / hyp

		return dx, dy

	def move(self):
		dx, dy = self.get_dxdy()

		if dx:
			self.rect.x += int(round(dx * self.game.dt * Zombie.SPEED))
			while self.rect.x < 0:
				self.rect.x += 1
			while self.rect.right > self.game.maxwidth:
				self.rect.x -= 1
			while pygame.sprite.spritecollide(self, self.game.allblocks, False):
				self.rect.x -= int(abs(dx) / dx)

		if dy:
			self.rect.y += int(round(dy * self.game.dt * Zombie.SPEED))
			while self.rect.y < 0:
				self.rect.y += 1
			while self.rect.bottom > self.game.maxheight:
				self.rect.y -= 1
			while pygame.sprite.spritecollide(self, self.game.allblocks, False):
				self.rect.y -= int(abs(dy) / dy)

	def get_angle_of_rotation(self):
		alpha = 0
		hor, vert = self.get_dxdy()

		if (hor, vert) != (0, 0):
			hyp = math.sqrt((hor**2) + (vert**2))
			ratio = vert / hyp
			
			if hor >= 0 and vert <= 0:
				alpha = -math.asin(ratio) * 180 / math.pi
			elif hor <= 0 and vert <= 0:
				alpha = -(math.acos(ratio) * 180 / math.pi + 90)
			elif hor <= 0 and vert >= 0:
				alpha = math.asin(ratio) * 180 / math.pi + 180
			elif hor >= 0 and vert >= 0:
				alpha = math.acos(ratio) * 180 / math.pi + 270

			alpha = int(alpha) % 360

		return alpha

	def rotate(self):
		alpha = self.get_angle_of_rotation()

		# Forcibly scale to normal size when rotating by multiples of 90deg because rotozoom enlarges sprite by 2px when rotating
		# by either 180deg or 270deg for some unknown reason
		oldcenter = self.rect.center
		if not(alpha % 90):
			self.image = pygame.transform.rotate(Zombie.IMG, alpha)
			self.image = pygame.transform.scale(self.image, (40, 40))
		else:
			self.image = pygame.transform.rotozoom(Zombie.IMG, alpha, 1)
		self.rect = self.image.get_rect(center=oldcenter)
		self.angle = alpha

		# Adjust rotation so that it doesn't collide with blocks
		new_alpha = alpha
		while pygame.sprite.spritecollide(self, self.game.allblocks, False):
			# Decide whether to revert clockwise or counterclockwise
			if (abs(alpha - self.angle)) < 180:
				new_alpha = (new_alpha - 1) % 360
			else:
				new_alpha = (new_alpha + 1) % 360
			
			if not(new_alpha % 90):
				self.image = pygame.transform.rotate(Zombie.IMG, new_alpha)
				self.image = pygame.transform.scale(self.image, (40, 40))
			else:
				self.image = pygame.transform.rotozoom(Zombie.IMG, alpha, 1)
			self.rect = self.image.get_rect(center=oldcenter)	
			self.angle = new_alpha

	def update(self):
		self.move()
		self.rotate()
		





class Player(pygame.sprite.Sprite):
	IMG = pygame.image.load('player.png')
	SPEED = 0.5

	def __init__(self, game, uid, x, y):
		self.game = game
		self.groups = game.allsprites, game.allplayers
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.image = Player.IMG
		self.rect = self.image.get_rect(topleft=(x, y))
		self.angle = 0

		self.uid = uid
		self.stick = self.game.joysticks[self.uid]


	def get_dxdy(self):
		dx, dy = 0, 0
		hor = self.stick.get_axis(0)
		vert = self.stick.get_axis(1)
		if abs(hor) < 0.1:
			hor = 0
		if abs(vert) < 0.1:
			vert = 0

		hyp = math.sqrt(hor ** 2 + vert ** 2)
		if hyp:
			dx = hor / hyp
			dy = vert / hyp

		return dx, dy

	def get_angle_of_rotation(self):
		alpha = 0
		hor, vert = 0, 0
		if abs(self.stick.get_axis(2)) >= 0.2:
			hor = self.stick.get_axis(2)
		if abs(self.stick.get_axis(3)) >= 0.2:
			vert = self.stick.get_axis(3)

		if (hor, vert) != (0, 0):
			hyp = math.sqrt((hor**2) + (vert**2))
			ratio = vert / hyp
			
			if hor >= 0 and vert <= 0:
				alpha = -math.asin(ratio) * 180 / math.pi
			elif hor <= 0 and vert <= 0:
				alpha = -(math.acos(ratio) * 180 / math.pi + 90)
			elif hor <= 0 and vert >= 0:
				alpha = math.asin(ratio) * 180 / math.pi + 180
			elif hor >= 0 and vert >= 0:
				alpha = math.acos(ratio) * 180 / math.pi + 270

			alpha = int(alpha) % 360

		return alpha

	def rotate(self):
		alpha = self.get_angle_of_rotation()

		# Forcibly scale to normal size when rotating by multiples of 90deg because rotozoom enlarges sprite by 2px when rotating
		# by either 180deg or 270deg for some unknown reason
		oldcenter = self.rect.center
		if not(alpha % 90):
			self.image = pygame.transform.rotate(Player.IMG, alpha)
			self.image = pygame.transform.scale(self.image, (40, 40))
		else:
			self.image = pygame.transform.rotozoom(Player.IMG, alpha, 1)
		self.rect = self.image.get_rect(center=oldcenter)
		self.angle = alpha

		# Adjust rotation so that it doesn't collide with blocks
		new_alpha = alpha
		while pygame.sprite.spritecollide(self, self.game.allblocks, False):
			# Decide whether to revert clockwise or counterclockwise
			if (abs(alpha - self.angle)) < 180:
				new_alpha = (new_alpha - 1) % 360
			else:
				new_alpha = (new_alpha + 1) % 360
			
			if not(new_alpha % 90):
				self.image = pygame.transform.rotate(Player.IMG, new_alpha)
				self.image = pygame.transform.scale(self.image, (40, 40))
			else:
				self.image = pygame.transform.rotozoom(Player.IMG, alpha, 1)
			self.rect = self.image.get_rect(center=oldcenter)	
			self.angle = new_alpha

	def move(self):
		dx, dy = self.get_dxdy()

		if dx:
			self.rect.x += int(round(dx * self.game.dt * Player.SPEED))
			while self.rect.x < 0:
				self.rect.x += 1
			while self.rect.right > self.game.maxwidth:
				self.rect.x -= 1
			while pygame.sprite.spritecollide(self, self.game.allblocks, False):
				self.rect.x -= int(abs(dx) / dx)

		if dy:
			self.rect.y += int(round(dy * self.game.dt * Player.SPEED))
			while self.rect.y < 0:
				self.rect.y += 1
			while self.rect.bottom > self.game.maxheight:
				self.rect.y -= 1
			while pygame.sprite.spritecollide(self, self.game.allblocks, False):
				self.rect.y -= int(abs(dy) / dy)

	def update(self):
		self.rotate()
		self.move()




class Block(pygame.sprite.Sprite):
	IMG = pygame.image.load('block.png')

	def __init__(self, game, x, y):
		self.game = game
		self.groups = game.allsprites, game.allblocks
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.image = Block.IMG
		self.rect = self.image.get_rect(topleft=(x, y))

	def update(self):
		pass


class Game:
	pygame.init()

	def __init__(self):
		self.screen = pygame.display.set_mode((0, 0))
		# self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.maxwidth, self.maxheight = 1600, 1200
		self.clock = pygame.time.Clock()
		self.dt = 0

		self.allsprites = pygame.sprite.Group()
		self.allplayers = pygame.sprite.Group()
		self.allblocks = pygame.sprite.Group()
		self.allzombies = pygame.sprite.Group()

		self.joysticks = []
		self.setup()

		for i in range(len(self.joysticks)):
			Player(self, i, 1000+100*i, 1000+200*i)
		self.camera = Camera(self)

	def find_player(self, uid):
		for player in self.allplayers:
			if player.uid == uid:
				return player
		return None

	def setup(self):
		self.setup_map()
		self.setup_joysticks()

	def setup_map(self):
		Block(self, 0, 0)
		Block(self, 100, 100)
		Block(self, 150, 100)
		Block(self, 150, 200)
		Block(self, 200, 100)
		Block(self, 750, 600)
		Block(self, 800, 600)
		Block(self, 800, 650)
		Block(self, 1200, 800)
		Block(self, 1550, 1150)

		Zombie(self, 600, 600)
		Zombie(self, 200, 200)
		Zombie(self, 800, 100)

	def setup_joysticks(self):
		pygame.joystick.init()

		for i in range(pygame.joystick.get_count()):
			self.joysticks.append(pygame.joystick.Joystick(i))
			self.joysticks[i].init()
			print(self.joysticks[i].get_name())

	def quit(self):
		pygame.quit()
		sys.exit()

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.quit()

			self.dt = self.clock.tick(60)
			self.update()
			self.draw()

	def update(self):
		self.allsprites.update()
		self.camera.update(self.find_player(0))

	def draw(self):
		self.screen.fill((0, 200, 0))
		for sprite in self.allsprites:
			self.screen.blit(sprite.image, self.camera.apply(sprite))
		pygame.display.flip()

if __name__ == '__main__':
	Game().run()