import pygame
import os
from time import sleep
from random import randint
pygame.init()

FPS = 60

window_width = 1280
window_height = 720

images = './images/' # where all images stored
music = './music/'   # where all music and sounds stored

wnd = pygame.display.set_mode((window_width, window_height ))

clock = pygame.time.Clock()

max_score = score = 0

#defining colors for conveiniece
		# R    G    B
white = (255, 255, 255)
red   = (255, 0,   0)
green = (0,   255, 0)
blue  = (0,   0,   255)
black = (0,   0,   0)
grey  = (150, 150, 150)


score_text = pygame.font.Font('./fonts/Sen-Bold.ttf', 24)

# Load a bus images 
bus_images = [ pygame.image.load(os.path.join(images, 'Hero/Bus/bus0' + str(x) + '.png')) for x in range(1, 5) ]
	 
# Load a car images
car_images = [ pygame.image.load(os.path.join(images, 'Hero/Car/car0' + str(x) + '.png'))  for x in range(1, 5)]

# list of enemy images loading with usage of list copmprehensions
# os.path.join is used for joining string './images/' with other strings like 'Enemies/dyno/walking'
# we will get something like './images/Enemies/dyno/walking/' and plus imagename that can vary
# In the end we get './images/Enemies/dyno/walking/skeleton-walking_<number>.png'
enemy_images = [ pygame.image.load(os.path.join(images, 'Enemies/dyno/walking','skeleton-walking_' + str(x) + '.png')) for x in range(21)]

menu_image = pygame.image.load(os.path.join(images, 'menu/menu.jpg'))


def display_score(score):
	score_text_surface = score_text.render("Score: " + str(score) + "\nMax Score: " + str(max_score), True, black)
	score_text_rect    = score_text_surface.get_rect()
	score_text_rect.right = window_width - 10
	score_text_rect.top   = 10
	wnd.blit(score_text_surface, score_text_rect)

def display_max_score(max_score):
	pass

def get_size(image, width):
	image_size = image.get_rect().size # get something like this: (400,200)
	return (width, int(image_size[1] * width / image_size[0]))

def resize_image(image, width):
	image_size = get_size(image, width)
	return pygame.transform.scale(image, image_size)

def is_out_of_screen(car):
	size = car.images[0].get_rect().size
	# x
	if car.x < 0 - int(size[0] / 2) or car.x > window_width - int(size[0] / 2):
		return True
	# y
	if car.y < 0 - int(size[1] / 2) or car.y > window_height - int(size[1] / 2):
		return True

	return False

def check_collision(hero, enemy):
	enemy_rect = enemy.rect
	hero_rect  = hero.rect

	if hero_rect.colliderect(enemy_rect) == 1:
		return True

	return False
		
def game_reset(hero, enemy):
	sleep(1)
	global score, max_score
	if score > max_score:
		max_score = score
	score = 0
	hero.crash()
	enemy.restore_position()




image_width = 200
car_images = list(map(resize_image, # Function that takes two arguments
					  car_images,   # First argument will be from this list
					  [ image_width for i in range(len(car_images)) ] ))	# Generate list that will be the second 
																	  		# argument is taken from this list  
				

enemy_images = list(map(resize_image, enemy_images, [ 200 for x in range(len(enemy_images)) ]))

menu_image = resize_image(menu_image, window_width)

class Background():
	def __init__(self):
		self.line_interval  = 150
		self.line_width     = 300
		self.line_height    = 50
		self.lines = [ pygame.Rect(0, int(window_height / 2) - int(self.line_height / 2), self.line_width, self.line_height)]

	def draw_back(self):
		wnd.fill(grey)

	def draw_lines(self):
		for rectangle in self.lines:
			pygame.draw.rect(wnd, white, rectangle)

	def draw(self):
		self.move_lines()
		self.draw_back()
		self.draw_lines()

	def append_line(self):
		while self.lines[-1].x < window_width:
			self.lines.append(
				pygame.Rect(self.lines[-1].x + self.line_width + self.line_interval,
				int(window_height / 2) - int(self.line_height / 2),
				self.line_width, self.line_height))

	def pop_line(self):
		if self.lines[0].x + self.line_width < 0:
			self.lines.pop(0)

	def move_lines(self):
		self.append_line()
		self.pop_line()

		for i in range(len(self.lines)):
			self.lines[i] = self.lines[i].move(-5, 0)

class Sound():
	def __init__(self):
		self.background_music_standard = './music/bgmusic.mp3'
		self.background_music_corona   = './music/corona.mp3'

		self.boom = pygame.mixer.Sound('./music/boom.wav')
		self.boom.set_volume(0.25)
		

	def play_standard(self):
		pygame.mixer.music.load(self.background_music_standard)
		pygame.mixer.music.set_volume(0.1)
		pygame.mixer.music.play()

	def play_corona(self):
		pygame.mixer.music.load(self.background_music_corona)
		pygame.mixer.music.set_volume(0.1)
		pygame.mixer.music.play()

	def crash(self):
		self.boom.play()

class Base():
	def __init__(self, x, y, images):
		self.x = x
		self.y = y
		self.images = images
		self.rect = images[0].get_rect()


	def draw(self, frame):
		wnd.blit(self.images[frame], (self.x, self.y))
		# pygame.draw.rect(wnd, green, self.rect)

class Hero(Base):
	def __init__(self):
		super().__init__(50, int(window_height / 2), car_images) # x, y, hero_images
		self.rect.size = (self.rect.size[0] - 40, self.rect.size[1] - 20) 
		s = self.images[0].get_rect().size
		self.rect.center = (self.x + int(s[0]/2), self.y + int(s[1]/2))

	def move(self, x, y):
		self.x += x
		self.y += y
		s = self.images[0].get_rect().size
		self.rect.center = (self.x + int(s[0]/2), self.y + int(s[1]/2))

	def restore_position(self):
		self.x = 50
		self.y = int(window_height / 2)

	def crash(self):
		self.restore_position()

class Enemy(Base):
	def __init__(self):
		super().__init__(
			int(window_width * 0.8),    # x
			int(window_height / 2),     # y
			enemy_images)  				# enemy_images
		self.rect.size = (self.rect.size[0] - 50, self.rect.size[1] - 45) 
		s = self.images[0].get_rect().size
		self.rect.center = (self.x + int(s[0]/2), self.y + int(s[1]/2))

	def move(self, x=-5, y=0):
		self.x += x
		self.y += y
		s = self.images[0].get_rect().size
		self.rect.center = (self.x + int(s[0]/2), self.y + int(s[1]/2) - 10)


	def restore_position(self):
		self.x = window_width + 150
		self.y = randint(0, window_height - self.rect.size[1])

	def draw(self, frame):
		if self.x + image_width < 0:
			self.restore_position()
		super().draw(frame)

sounds = Sound()
bg = Background()

def game_menu():

	text_size = 100
	text_resize_speed = 1

	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				intro = False


		textMenu        = pygame.font.Font('./fonts/Sen-Bold.ttf', 140)
		textMenuSurface = textMenu.render("Main Menu", True, black)
		textMenuRect    = textMenuSurface.get_rect()
		textMenuRect.center = (int(window_width/2), int(window_height/6))


		textEnter        = pygame.font.Font('./fonts/Sen-Bold.ttf', text_size) # Get Font
		textEnterSurface = textEnter.render("Press Enter", True, black) # Get Rendered text
		textEnterRect    = textEnterSurface.get_rect()
		textEnterRect.center = (int(window_width/2), int(window_height/1.5)) # Set positions 


		wnd.blit(menu_image, (0,0))
		wnd.blit(textMenuSurface, textMenuRect)
		wnd.blit(textEnterSurface, textEnterRect)

		text_size += text_resize_speed

		if text_size > 110:
			text_resize_speed *= -1
		elif text_size < 100:
			text_resize_speed *= -1

		pygame.display.update()

		clock.tick(60)
		
def game_pause():
	pause = True
	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pause = False

		textMenu        = pygame.font.Font('./fonts/Sen-Bold.ttf', 140)
		textMenuSurface = textMenu.render("Pause", True, black)
		textMenuRect    = textMenuSurface.get_rect()
		textMenuRect.center = (int(window_width/2), int(window_height/4))

		wnd.blit(textMenuSurface, textMenuRect)
		pygame.display.update()

def game_loop():

	car = Hero()
	enemy = Enemy()

	x = window_width / 2
	y = window_height / 2

	vel = 3
	vel_x = 0
	vel_y = 0
	car_next_tick = pygame.time.get_ticks()
	enemy_next_tick = pygame.time.get_ticks()
	car_frame = 0
	enemy_frame = 0

	global score, max_score

	bg.draw()
	car.draw(car_frame)
	enemy.draw(enemy_frame)
	pygame.display.update()


	sleep(0.5)
	while True:

		clock.tick(FPS)
		
		for event in pygame.event.get():
			print(event)

			if event.type == pygame.QUIT:
				exit()

			elif event.type == pygame.KEYUP and (not vel_x == 0 or not vel_y == 0):
				if event.key == pygame.K_d:
					vel_x += -vel
				elif event.key == pygame.K_a:
					vel_x -= -vel
				elif event.key == pygame.K_w:
					vel_y -= -vel
				elif event.key == pygame.K_s:
					vel_y += -vel

			elif event.type == pygame.KEYDOWN:

				if event.key == pygame.K_ESCAPE:
					game_pause()
					vel_y = vel_x = 0
					enemy_next_tick = car_next_tick = pygame.time.get_ticks()

				elif event.key == pygame.K_d:
					vel_x += vel
				elif event.key == pygame.K_a:
					vel_x -= vel
				elif event.key == pygame.K_w:
					vel_y -= vel
				elif event.key == pygame.K_s:
					vel_y += vel
					
				#music section
				elif event.key == pygame.K_p:
					sounds.play_corona()
				elif event.key == pygame.K_o:
					sounds.play_standard()
			

		if is_out_of_screen(car):
			sounds.crash()
			car.crash()
			car_next_tick = pygame.time.get_ticks()
			enemy_next_tick = pygame.time.get_ticks()


		# Car Animation
		if pygame.time.get_ticks() > car_next_tick:
			if vel_x > 0:
				car_next_tick += 80
			elif vel_x < 0:
				car_next_tick += 120
			else:
				car_next_tick += 100

			car_frame = (car_frame + 1) % 4

		#Enemy Animation
		if pygame.time.get_ticks() > enemy_next_tick:
			enemy_next_tick += 25
			enemy_frame = (enemy_frame + 1) % 21


		

		bg.draw()
		car.move(vel_x, vel_y)
		car.draw(car_frame)
		enemy.move()
		enemy.draw(enemy_frame)

		score += 1
		display_score(score)
		display_max_score(max_score)

		pygame.display.update()

		if check_collision(car, enemy):
			game_reset(car, enemy)




game_menu()
game_loop()