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


#defining colors for conveiniece
		# R    G    B
white = (255, 255, 255)
red   = (255, 0,   0)
green = (0,   255, 0)
blue  = (0,   0,   255)
black = (0,   0,   0)
grey  = (150, 150, 150)

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
	enemy_rect = enemy.images[0].get_rect()
	enemy_rect.x = enemy.x
	enemy_rect.y = enemy.y

	hero_rect  = hero.images[0].get_rect()
	hero_rect.x = hero.x
	hero_rect.y = hero.y

	if hero_rect.colliderect(enemy_rect) == 1:
		sleep(1)
		car.crash()
		enemy.restore_position()



image_width = 200 
car_images = list(map(resize_image, # Function that takes two arguments
					  car_images,   # First argument will be from this list
					  [ image_width for i in range(len(car_images)) ] ))	# Generate list that will be the second 
																	  		# argument is taken from this list  
				

enemy_images = list(map(resize_image, enemy_images, [ 200 for x in range(len(enemy_images)) ]))


#old version of resizing images

# for i in range(len(car_images)):
# 	car_images[i] = resize_image((car_images[i], 200))


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
		if self.lines[-1].x < window_width:
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
		# s = self.images[0].get_rect().size
		# pygame.draw.rect(wnd, green, (self.x, self.y, s[0], s[1]))


class Hero(Base):
	def __init__(self):
		super().__init__(50, int(window_height / 2), car_images) # x, y, hero_images
	
	def move(self, x, y):
		self.x += x
		self.y += y

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
	def move(self, x=-5, y=0):
		self.x += x
		self.y += y

	def restore_position(self):
		self.x = window_width
		self.y = int(window_height / 2)

	def draw(self, frame):
		if self.x + image_width < 0:
			self.x = window_width + 150
			self.y = randint(0, window_height - self.rect.size[1])
		super().draw(frame)


sounds = Sound()
car = Hero()
enemy = Enemy()
bg = Background()

print(bg.lines)

x = window_width / 2
y = window_height / 2

vel = 3
vel_x = 0
vel_y = 0
car_next_tick = pygame.time.get_ticks()
enemy_next_tick = pygame.time.get_ticks()
car_frame = 0
enemy_frame = 0

while True:

	clock.tick(FPS)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				vel_x += vel
			elif event.key == pygame.K_LEFT:
				vel_x -= vel
			elif event.key == pygame.K_UP:
				vel_y -= vel
			elif event.key == pygame.K_DOWN:
				vel_y += vel
				
			#music section
			elif event.key == pygame.K_p:
				sounds.play_corona()
			elif event.key == pygame.K_o:
				sounds.play_standard()


		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT:
				vel_x += -vel
			elif event.key == pygame.K_LEFT:
				vel_x -= -vel
			elif event.key == pygame.K_UP:
				vel_y -= -vel
			elif event.key == pygame.K_DOWN:
				vel_y += -vel

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


	check_collision(car, enemy)
	wnd.fill(white)
	bg.draw()
	car.move(vel_x, vel_y)
	car.draw(car_frame)
	enemy.move()
	enemy.draw(enemy_frame)
	pygame.display.update()
