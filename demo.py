import pygame
import os


pygame.init()

FPS = 60

window_width = 1280
window_height = 720

images = './images/'
music = './music/'

wnd = pygame.display.set_mode((window_width, window_height ))

clock = pygame.time.Clock()

white = (255, 255, 255)
red   = (255, 0,   0)
green = (0,   255, 0)
blue  = (0,   0,   255)
black = (0,   0,   0)

bus_images = [
	pygame.image.load(os.path.join(images, 'Hero/Bus/bus01.png')),
	pygame.image.load(os.path.join(images, 'Hero/Bus/bus02.png')),
	pygame.image.load(os.path.join(images, 'Hero/Bus/bus03.png')),
	pygame.image.load(os.path.join(images, 'Hero/Bus/bus04.png'))
]

car_images = [
	pygame.image.load(os.path.join(images, 'Hero/Car/car01.png')),
	pygame.image.load(os.path.join(images, 'Hero/Car/car02.png')),
	pygame.image.load(os.path.join(images, 'Hero/Car/car03.png')),
	pygame.image.load(os.path.join(images, 'Hero/Car/car04.png'))
]

enemy_images = [ pygame.image.load(os.path.join(images, 'Enemies/dyno/walking','skeleton-walking_' + str(x) + '.png')) for x in range(21)]

def get_size(image, width):
	image_size = image.get_rect().size # (400,200)
	return (width, int(image_size[1] * width / image_size[0]))
	

# def resize_image(image):
# 	image_size = get_size(image, 200)
# 	return pygame.transform.scale(image, image_size)

def resize_image(image, width):
	image_size = get_size(image, width)
	return pygame.transform.scale(image, image_size)



car_images = list(map(resize_image, car_images, [ 200 for x in range(len(car_images)) ]))
enemy_images = list(map(resize_image, enemy_images, [ 200 for x in range(len(enemy_images)) ]))

# for i in range(len(car_images)):
# 	car_images[i] = resize_image((car_images[i], 200))


class Base():
	def __init__(self, x, y, images):
		self.x = x
		self.y = y
		self.images = images

	def draw(self, frame):
		wnd.blit(self.images[frame], (self.x, self.y))


class Hero(Base):
	def __init__(self):
		super().__init__(50, int(window_height / 2), car_images) # x, y, hero_images
	
	def move(self, x, y):
		self.x += x
		self.y += y


class Enemy(Base):
	def __init__(self):
		super().__init__(
			int(window_width * 0.8),    # x
			int(window_height / 2),     # y
			enemy_images)  				# enemy_images 

car = Hero()
enemy = Enemy()

x = window_width / 2
y = window_height / 2

vel = 3
vel_x = 0
vel_y = 0
car_next_tick = 100
enemy_next_tick = 50
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

		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT:
				vel_x += -vel
			elif event.key == pygame.K_LEFT:
				vel_x -= -vel
			elif event.key == pygame.K_UP:
				vel_y -= -vel
			elif event.key == pygame.K_DOWN:
				vel_y += -vel

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


	wnd.fill(white)
	car.move(vel_x, vel_y)
	car.draw(car_frame)
	enemy.draw(enemy_frame)
	pygame.display.update()
