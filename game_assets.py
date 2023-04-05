import pygame
from pygame import *
from vec2d import *
from random import randint
from menu_assets import Color

class Actor(object):
	_instances = set()
	def __init__(self, pos=vec2d(0,0), dim=(0,0)):
		Actor._instances.add(self)	
		self.pos = vec2d(pos[0],pos[1])
		self.rect = pygame.Rect((0,0), dim)	
		self.color = (255,255,255)	
		self.velocity = vec2d(0,0)	
	def draw(self, screen):
		pygame.draw.rect(screen, self.color, self.get_rect())
	def get_rect(self):
		return pygame.Rect(self.pos.inttup(), (self.rect.width, self.rect.height))
	def delete(self):
		Actor._instances.remove(self)

class Faller(Actor):
	_instances = set()
	def __init__(self):
		size = randint(40,150)
		super(Faller, self).__init__(pos=vec2d(randint(0 ,1366 - size), -size),dim=(size,size))
		Faller._instances.add(self)
		self.color = Color.hsl_to_rgb(Color.random_hsl(low=0.5,high=0.5))
		self.acceleration = 2400.0/(self.rect.width * self.rect.height) 
	def update(self):
		self.velocity += vec2d( 0, self.acceleration)
		if self.velocity.get_length_sqrd != 0:	
			self.velocity.length *= 0.8
		self.pos += self.velocity
	def draw(self, screen):
		pygame.draw.rect(screen, self.color, self.get_rect())
	def delete(self):
		super(Faller,self).delete()
		Faller._instances.remove(self)
	
class Dodger(Actor):	
	def __init__(self):
		self.pos = vec2d(400,550)
		self.rect = pygame.Rect((0,0), (5,5))	
		self.color    = ( 155, 255, 255)
		self.velocity = vec2d(0,0)	
		self.friction = 0.8
	def update(self):
		if self.velocity.length != 0:
			self.velocity.length *= self.friction
		if self.pos.x + self.velocity.x > 0 and self.pos.x + self.velocity.x + self.rect.width < 1366:
			self.pos.x += self.velocity.x
		if self.pos.y + self.velocity.y > 0 and self.pos.y + self.velocity.y + self.rect.height < 768:
			self.pos.y += self.velocity.y
	def draw(self, screen):
		pygame.draw.rect(screen, self.color, self.get_rect())
	def get_rect(self):
		return pygame.Rect(self.pos.inttup(), (self.rect.width, self.rect.height))

class FallerAdder(object):
	init_increase_rate = 300
	increase_rate = 300
	
	def __init__(self):
		self.counter = 0
		self.amount = 0	
		FallerAdder.increase_rate = FallerAdder.init_increase_rate
	
	def update(self):
		self.counter += 1
		
		if self.counter >= FallerAdder.increase_rate:
			self.counter -= FallerAdder.increase_rate
			self.amount += 1
		
		while len(Faller._instances) < self.amount:
			Faller()
		
	def reset(self):
		self.amount = 0
		FallerAdder.increase_rate = FallerAdder.init_increase_rate	
		Faller._instances = set()
		Actor._instances = set()


