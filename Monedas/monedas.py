import pygame, random
from random import randint
from pathlib import Path

WIDTH = 800
HEIGHT = 550
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monedas")
clock = pygame.time.Clock()
current_path = Path.cwd()
file_path = current_path / 'highscore.txt'

def draw_text(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, percentage):
	BAR_LENGHT = 100
	BAR_HEIGHT = 10
	fill = (percentage / 100) * BAR_LENGHT
	border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
	fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surface, GREEN, fill)
	pygame.draw.rect(surface, WHITE, border, 2)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("img/player.png").convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 2
		self.rect.bottom = HEIGHT - 10
		self.speed_x = 0
		self.shield = 100
		self.jumping = False
		self.Y_GRAVITY = 1
		self.JUMP_HEIGHT = 20
		self.Y_VELOCITY = self.JUMP_HEIGHT

	def update(self):
		self.speed_x = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_a]:
			self.speed_x = -10
		if keystate[pygame.K_d]:
			self.speed_x = 10
		if keystate[pygame.K_f]:
			self.jumping = True
		self.rect.x += self.speed_x
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

class Coins(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = coins_images[0]
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-150, -100)
		self.speedy = random.randrange(1, 10)
		self.speedx = 0

	def update(self):
		self.rect.y += self.speedy
		#self.rect.x += self.speedx
		if self.rect.top > HEIGHT + 10:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-150, - 100)
			self.speedy = random.randrange(1, 10)

class Diam(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = random.choice(diam_images)
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-150, -100)
		self.speedy = random.randrange(1, 10)
		self.speedx = 0

	def update(self):
		self.rect.y += self.speedy
		#self.rect.x += self.speedx
		if self.rect.top > HEIGHT + 20:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-150, - 100)
			self.speedy = random.randrange(1, 10)

def show_go_screen():
	
	screen.blit(background, [0,0])
	draw_text(screen, "Monedas", 65, WIDTH // 2, HEIGHT // 4)
	draw_text(screen, "Colecta las monedas", 20, WIDTH // 2, HEIGHT // 2)
	draw_text(screen, "Press Q", 20, WIDTH // 2, HEIGHT * 3/4)
	draw_text(screen, "Created by: Francisco Carvajal", 10,  60, 500)
	
	
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					waiting = False

coins_images = []
coins_list = ["img/mon.png"]
for img in coins_list:
	coins_images.append(pygame.image.load(img).convert())

diam_images = []
diam_list = ["img/diam.png", "img/diam2.png",]
for img in diam_list:
	diam_images.append(pygame.image.load(img).convert())

def get_high_score():
	with open(file_path,'r') as file:
		return file.read()

def show_game_over_screen():
	screen.blit(background, [0,0])
	if highest_score <= score:
		draw_text(screen, "¡high score!", 60, WIDTH  // 2, HEIGHT * 1/4)
		draw_text(screen, "score: "+str(score), 30, WIDTH // 2, HEIGHT // 2)
		draw_text(screen, "Press Q", 20, WIDTH // 2, HEIGHT * 4/5)
	else:
		draw_text(screen, "score: "+str(score), 60, WIDTH // 2, HEIGHT * 1/3)
		draw_text(screen, "Press Q", 20, WIDTH // 2, HEIGHT * 2/3)

	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					waiting = False

# Cargar imagen de fondo
background = pygame.transform.scale(pygame.image.load("img/fond.png").convert(),(800,550))

### high score

try:
	highest_score = int(get_high_score())
except:
	highest_score = 0


game_over = False
running = True
start = True
while running:
	if game_over:

		show_game_over_screen()
		game_over = False
		all_sprites = pygame.sprite.Group()
		coins_list = pygame.sprite.Group()
		diam_list = pygame.sprite.Group()

		player = Player()
		all_sprites.add(player)
		for i in range(8):
			coin = Coins()
			all_sprites.add(coin)
			coins_list.add(coin)
		#all_sprites.add(player)
		for i in range(4):
			diam = Diam()
			all_sprites.add(diam)
			diam_list.add(diam)

		score = 0
		

	if start:
		show_go_screen()
		start = False
		#game_over = False
		all_sprites = pygame.sprite.Group()
		coins_list = pygame.sprite.Group()
		diam_list = pygame.sprite.Group()

		player = Player()
		all_sprites.add(player)
		for i in range(8):
			coin = Coins()
			all_sprites.add(coin)
			coins_list.add(coin)
		#all_sprites.add(player)
		for i in range(4):
			diam = Diam()
			all_sprites.add(diam)
			diam_list.add(diam)

		score = 0


	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		#elif event.type == pygame.KEYDOWN:
			#if event.key == pygame.K_f:
				#player.shoot()

	if player.jumping:
		player.rect.bottom -= player.Y_VELOCITY
		player.Y_VELOCITY -= player.Y_GRAVITY
		if player.Y_VELOCITY < - player.JUMP_HEIGHT:
			player.jumping = False
			player.Y_VELOCITY = player.JUMP_HEIGHT

	all_sprites.update()

	if coin.rect.top > HEIGHT:
		score -= 10
	if diam.rect.top > HEIGHT:
		score -= 100

	#colisiones - coins - player
	hits = pygame.sprite.spritecollide(player, coins_list, True)
	for hit in hits:
		score += 10
		
		
		coin = Coins()
		all_sprites.add(coin)
		coins_list.add(coin)

	#colisiones - diam - player
	hits2 = pygame.sprite.spritecollide(player, diam_list, True )
	for hit in hits2:
		score += 100
		
		
		diam = Diam()
		all_sprites.add(diam)
		diam_list.add(diam)
		
	"""
	# dtención del juego en t = () en mlseg	
	now = pygame.time.get_ticks()
	if now > 16000:
		game_over = True"""
	
	screen.blit(background, [0, 0])

	all_sprites.draw(screen)

	#Marcador
	draw_text(screen, str(score), 25, WIDTH // 2, 10)

	# Escudo.
	draw_shield_bar(screen, 5, 5, player.shield)

	pygame.display.flip()