import pygame
pygame.init()
from random import randint, random, uniform

class Color(object):
	BLACK     = (  0,  0,  0)
	BLACKGREY = ( 63, 63, 63)
	GREY      = (127,127,127)
	GREYWHITE = (191,191,191)	
	WHITE     = (255,255,255)
	
	RED       = (255,  0,  0)
	GREEN     = (  0,255,  0)
	BLUE      = (  0,  0,255)
	
	YELLOW    = (255,255,  0)
	CYAN      = (  0,255,255)
	MAGENTA   = (255,  0,255)
	
	@staticmethod
	def random_rgb(low=0,high=255):
		return (randint(low,high),randint(low,high),randint(low,high))
	
	@staticmethod
	def random_hsl(low=0.0,high=1.0):
		h = randint(0,359)
		s = random()
		l = uniform(low,high) 
		return (h,s,l)

	@staticmethod
	def rgb_to_hsl(rgb):
		r, g, b = rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0
		cmax, cmin = max(r, g, b), min(r, g, b)
		delta = cmax - cmin
		
		if delta == 0:
			hue = 0
		elif cmax == r:
			hue = (60 * ((g - b) / delta) + 360) % 360
		elif cmax == g:
			hue = (60 * ((b - r) / delta) + 120) % 360
		else:
			hue = (60 * ((r - g) / delta) + 240) % 360
		
		lightness = (cmax + cmin) / 2.0
		if delta == 0:
			saturation = 0
		else:
			saturation = delta / (1 - abs(2 * lightness - 1))
		
		return (hue, saturation, lightness)
	
	@staticmethod
	def hsl_to_rgb(hsl):
		h,s,l = hsl[0],hsl[1],hsl[2]
		c = (1 - abs(2 * l - 1)) * s
		x = c * (1 - abs((h / 60) % 2 - 1))
		m = l - c/2.0
		
		if h < 60:
			r, g, b = c, x, 0
		elif h < 120:
			r, g, b = x, c, 0
		elif h < 180:
			r, g, b = 0, c, x
		elif h < 240:
			r, g, b = 0, x, c
		elif h < 300:
			r, g, b = x, 0, c
		else:
			r, g, b = c, 0, x
			
		r, g, b = (r+m)*255, (g+m)*255, (b+m)*255
		return (int(r), int(g), int(b))

class Label(object):
	def __init__(self, rect=pygame.Rect((0,0),(10,10)), text = "Label", color = Color.WHITE,font_size=25,text_color=Color.BLACK,):
		self.font = pygame.font.Font(None,font_size)	
		self.rect       = rect
		self.text       = text 
		self.color      = color	
		self.text_color = text_color 
		self.text_image = self.font.render(self.text, True, self.text_color)	
	def draw(self, screen):
		pygame.draw.rect(screen, self.color, self.rect)
		
		temp = self.rect.center
		rect = self.text_image.get_rect()
		temp = (temp[0] - rect.width/2, temp[1] - rect.height/2)	
		
		screen.blit(self.text_image, temp)
	
	def set_text(self, text):
		self.text = text
		self.reload_text_image()

	def set_color(self, color):
		self.color = color

	def set_text_color(self, color):
		self.text_color = color
		self.reload_text_image()
	
	def reload_text_image(self):
		self.text_image = self.font.render(self.text, True, self.text_color)
	
	def set_font(self, font):
		self.font = font
		self.reload_text_image()
	

class Button(Label):
	def __init__(self, rect, text = "Button", color = Color.WHITE, font_size=25, function = None, text_color=Color.BLACK):
		super(Button, self).__init__(rect,text,color,font_size,text_color)
		self.function = function
	
	def execute_function(self):
		if self.function == None:
			print("no function assigned to this button")	
		else:	
			self.function()	
		
	def set_function(self, function):
		self.function = function
	
class Menu(object):
	def __init__(self):
		self.buttons              = {}
		self.labels               = {}
		self.background_color     = Color.BLACK
			
	def draw(self, screen):
		screen.fill(self.background_color)
		for label in self.labels:
			self.labels[label].draw(screen)	
		for button in self.buttons:
			self.buttons[button].draw(screen)
		
	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				for button in self.buttons:
					if self.buttons[button].rect.collidepoint(event.pos):
						self.buttons[button].execute_function()	

	def process(self):
		pass
