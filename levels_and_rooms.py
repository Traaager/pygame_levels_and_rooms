import pygame as pg
from pygame.locals import *

pg.init()

disp  = pg.display.set_mode((512, 256))
clock = pg.time.Clock()

SPEED = 5

IMG_STREET = pg.image.load("level1 street.png").convert()
IMG_HOUSE1 = pg.image.load("level1 house 1.png").convert()
IMG_HOUSE2 = pg.image.load("level1 house 2.png").convert()
IMG_PLAYER = pg.image.load("player.png").convert_alpha()
IMG_COIN   = pg.image.load("coin.png").convert_alpha()
IMG_ENEMY  = pg.image.load("enemy.png").convert_alpha()

levels = {
	"street" : {
		"bg" : IMG_STREET,
		"portals" : [
			[( 65, 60), "house1", (430, 200)],
			[(339, 82), "house2", ( 47, 195)],
			[(450, 82), "house2", (430, 180)]
		],
		"coins" : [(20, 20), (70, 130), (170, 40)],
		"enemies" : [[100, 100]]
	},
	"house1" : {
		"bg" : IMG_HOUSE1,
		"portals" : [
			[(430, 200), "street", (65, 60)]
		],
		"coins" : [],
		"enemies" : []
	},
	"house2" : {
		"bg" : IMG_HOUSE2,
		"portals" : [
			[( 47, 195), "street", (339, 82)],
			[(430, 180), "street", (450, 82)]
		],
		"coins" : [],
		"enemies" : [
			[200, 200],
			[300, 100]
		]
	}
}

current_level = levels["street"]

x = y = 100
xvel = yvel = 0

is_pressed = False

running = True
while running:
	disp.blit(current_level["bg"], (0, 0))
	for e in pg.event.get():
		if e.type == QUIT: running = False
		if e.type == KEYDOWN:
			if e.key == K_ESCAPE: running = False

	key = pg.key.get_pressed()
	if key[K_a]:
		xvel = -SPEED
	elif key[K_d]:
		xvel = SPEED
	else:
		xvel = 0

	if key[K_w]:
		yvel = -SPEED
	elif key[K_s]:
		yvel = SPEED
	else:
		yvel = 0

	x += xvel
	y += yvel

	if not is_pressed:
		if key[K_SPACE]:
			for portal in current_level["portals"]:
				if pg.Rect(x, y, 50, 50).collidepoint(portal[0]):
					x, y = portal[2]
					current_level = levels[portal[1]]
					is_pressed = True
	else:
		if not key[K_SPACE]:
			is_pressed = False

	disp.blit(IMG_PLAYER, (x, y))
	
	for coin in current_level["coins"]:
		if pg.Rect(x, y, 50, 50).collidepoint(coin):
			current_level["coins"] = [c for c in current_level["coins"] if c is not coin]
		disp.blit(IMG_COIN, coin)

	for enemy in current_level["enemies"]:
		enemy[0] -= (enemy[0] - x) * 0.1
		enemy[1] -= (enemy[1] - y) * 0.1
		disp.blit(IMG_ENEMY, enemy)


	pg.display.set_caption(f"{pg.mouse.get_pos()}")

	clock.tick(60)
	pg.display.update()

pg.quit()		
