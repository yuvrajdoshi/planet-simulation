import pygame
import math 

pygame.init()

width , height  =  800 , 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Solar System Sim')

white = (255,255,255)
yellow = (255,255,0)
blue = (100,149,237)
red = (138,59,80)
grey = (80,78,81)
brown = (165,0,0)

font = pygame.font.SysFont("comicsans" , 22 )


class Planet : 
	astro_unit = (1.496e8 * 1000) 
	G = (6.67428e-11)
	scale =  175 / astro_unit  #1 AU = 100px
	timestep = 60*60*24 #1 day  

	def __init__(self,x,y,radius,colour,mass):
		self.x = x
		self.y = y
		self.colour = colour
		self.radius = radius 
		self.mass = mass

		self.orbit = []
		self.is_sun = False 
		self.distance_to_sun = 0

		self.x_vel = 0
		self.y_vel = 0 

	def draw(self,win):
		x =self.x * self.scale + width/2
		y =self.y * self.scale + height/2
		pygame.draw.circle(win, self.colour, (x,y) ,self.radius)

	def attraction(self,other):
		other_x,other_y = other.x , other.y
		distance_x = other.x - self.x
		distance_y = other.y - self.y
		distance = math.sqrt(distance_x**2 + distance_y**2)

		if other.is_sun:
			self.distance_to_sun = distance 

		force = self.G * self.mass * other.mass / distance**2
		theta = math.atan2(distance_y , distance_x)
		force_x = math.cos(theta) * force 
		force_y = math.sin(theta) * force
		return force_x , force_y

	def update_position(self,planets):
		total_fx = total_fy = 0
		for planet in planets : 
			if self == planet:
				continue 

			fx , fy = self.attraction(planet)
			total_fx +=fx
			total_fy +=fy

		self.x_vel += total_fx / self.mass * self.timestep
		self.y_vel += total_fy/ self.mass * self.timestep


		self.x += self.x_vel *self.timestep
		self.y += self.y_vel * self.timestep
		self.orbit.append((self.x,self.y))

def main():
	run = True 
	clock = pygame.time.Clock()

	sun = Planet(0,0,30,yellow,1.98892 * 10**30)
	sun.is_sun = True 


	earth = Planet(-1*Planet.astro_unit,0,14,blue,5.9742*10**24)
	earth.y_vel = 29.783 * 1000
	
	mars = Planet(-1.5224*Planet.astro_unit , 0,12 ,red,6.39*10**23)
	mars.y_vel = 24.077 * 1000 

	mercury = Planet(- 0.387 * Planet.astro_unit , 0 ,8,grey, 3.30*10**23)
	mercury.y_vel = 47.4 * 1000

	venus = Planet( - 0.723 * Planet.astro_unit , 0, 14 , white,4.8685 *10**24)
	venus.y_vel = -35.02 * 1000

	jupiter = Planet( - 1.9 * Planet.astro_unit , 0,15 ,brown , 1.898 * 10**27)
	jupiter.y_vel = 21.232 * 1000

	planets = [sun , earth , mars ,mercury ,venus, jupiter]


	while run:
		clock.tick(60)
		window.fill((0,0,0))
#		pygame.display.update()



		for event in pygame.event.get():
			if event.type == pygame.QUIT :
				run = False

		for planet in planets:
			planet.update_position(planets)
			planet.draw(window)

		pygame.display.update()


	pygame.quit()

main()