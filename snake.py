import math 
import random
import pygame
import tkinter as tk
from tkinter import messagebox

#
class cube(object):
	rows = 20
	w = 500
	def __init__(self,start,dinx=1,dirny=0,color=(255,0,0)):  #default x is 1 coz to move in 1 direction
		self.pos = start
		self.dirnx = 1
		self.dirny = 0
		self.color = color

	def move(self, dirnx, dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
	
	def draw(self,surface,eyes=False):
		dis = self.w // self.rows
		i = self.pos[0]  #rows
		j = self.pos[1]	 #cols
		
		pygame.draw.rect(surface,self.color, (i*dis+1,j*dis+1,dis-2,dis-2))  #draw inside of square a bit
		#optional part to draw eyes
		if eyes:
			centre = dis//2
			radius = 3
			circleMiddle = (i*dis+centre-radius,j*dis+8)
			circleMiddle2 = (i*dis+dis-radius*2, j*dis+8)
			pygame.draw.circle(surface,(0,0,0),circleMiddle,radius)
			pygame.draw.circle(surface,(0,0,0),circleMiddle2,radius)

#parts or cube combined together to create a snake, so snake object will contain cube object
class snake(object):
	#list of cubes is snake body
	body = []
	turns = {}

	def __init__(self,color,pos):
		self.color = color

		#head cube positon is cube head
		self.head = cube(pos) 
		self.body.append(self.head)  #append head to the body

		#direction for x and y anyone one value at a time as snake will be moving in any one direction at a time
		self.dirnx = 0
		self.dirny = 1 

	def move(self):
		#once head turns every cube in body has to turn
		
		#look for the event
		for event in pygame.event.get():
			#if event is quit quit the game
			if event.type == pygame.QUIT:
				pygame.quit()

			#gets dictionary of all key values and if they were pressed or not
			keys = pygame.key.get_pressed()

			for key in keys:

				#works like graph if to be moved then x must be negative, if down then y negative..
				if keys[pygame.K_LEFT]:
					self.dirnx = -1
					self.dirny = 0
					#to remember when we turned so tail can turn
					self.turns[self.head.pos[:]] = [self.dirnx,self.dirny] #pos of head when turned

				elif keys[pygame.K_RIGHT]:
					self.dirnx = 1
					self.dirny = 0
					self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]

				elif keys[pygame.K_UP]:
					self.dirnx = 0
					self.dirny = -1
					self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]

				elif keys[pygame.K_DOWN]:
					self.dirnx = 0
					self.dirny = 1
					self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]

		#turn when cube is that location
		#get index and cube object from body
		for i,c in enumerate(self.body):
			p = c.pos[:]   #grab positon of cube
			if p in self.turns:  #check if cube is in our turn list
				turn = self.turns[p]
				c.move(turn[0],turn[1])  #grab turn x,y and move 
				if i == len(self.body)-1:  #if on last cube
					self.turns.pop(p)		#remove turn

			#if pos is not in list we still need to move in that direction
			else:
				#check postion and edge of the screen
				if c.dirnx == -1 and c.pos[0] <= 0:c.pos = (c.rows-1, c.pos[1])
				elif c.dirnx == 1 and c.pos[0] >= c.rows-1 :c.pos = (0,c.pos[1])
				elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
				elif c.dirny == -1 and c.pos[1] <= 0:c.pos = (c.pos[0],c.rows-1)
				else:c.move(c.dirnx,c.dirny)  #if cube at not to any edge then continue in same direction



	def reset(self,pos):
		#new head at position
		self.head = cube(pos)
		self.body = []
		self.body.append(self.head)
		self.turns ={}
		self.dirnx = 0
		self.dirny = 1

	#add snack to the tail
	def addCube(self):
		tail = self.body[-1]

		dx,dy = tail.dirnx,tail.dirny

		#check direction of tail moving to add the cube
		if dx == 1 and dy == 0:
			self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
		elif dx == -1 and dy == 0:
			self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
		elif dx ==0 and dy == 1:
			self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
		elif dx == 0 and dy == -1:
			self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

		#move cube along with the body of the snake
		self.body[-1].dirnx = dx
		self.body[-1].dirny = dy

	def draw(self,surface):
		for i,c in enumerate(self.body):
			if i==0:
				c.draw(surface,True)  #if cube is 1st one in the list draw its eyes :)
			else:
				c.draw(surface)

def drawGrid(w, rows, surface):
	sizeBtwn = w//rows

	x = 0
	y = 0
	for i in range(rows):
		x = x + sizeBtwn
		y = y + sizeBtwn

		#draws 2 lines for every loop
		#horizontal_line
		pygame.draw.line(surface , (255,255,255), (x,0), (x,w))     #onSurface with color and start pos and end pos
		#vertical_line
		pygame.draw.line(surface, (255,255,255), (0,y), (w,y))


def redrawWindow(surface):
	global rows, width, s, snack
	surface.fill((0,0,0))
	s.draw(surface)
	snack.draw(surface)
	drawGrid(width, rows, surface)
	pygame.display.update()


#food for snake
def randomSnack(rows, items):
	positons = items.body

	while True:
		x = random.randrange(rows)
		y = random.randrange(rows)

		#check if new pos is same as current position of snake
		if len(list(filter(lambda z:z.pos == (x,y), positons))) > 0:
			continue
		else:
			break
	return (x,y)

def messageBox(message, content):
	#new window on top any other
	root = tk.Tk()
	root.attributes("-topmost", True)
	root.withdraw()  #invisible
	messagebox.showinfo(message, content)

	try:
		root.destroy()
	except:
		pass

def main():
	global width, rows, s, snack
	width = 500
	rows = 20
	win = pygame.display.set_mode((width,width))
	s = snake((255,0,0),(10,10))
	snack = cube(randomSnack(rows,s), color=(0,255,0))
	flag = True

	clock = pygame.time.Clock()

	while flag:
		pygame.time.delay(50)
		clock.tick(10)   #run with 10 frame per second
		s.move()
		#check if head has eaten the snack if yes add cube to body
		if s.body[0].pos == snack.pos:
			s.addCube()
			snack = cube(randomSnack(rows,s), color=(0,255,0))

		for x in range(len(s.body)):
			#loop through every cube of sanke body
			if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
				Score ="You Score is "+str(len(s.body))
				messageBox('PySnake',Score)
				s.reset((10,10))
				break

		redrawWindow(win)
main()