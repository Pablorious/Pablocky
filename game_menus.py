from menu_assets import *
from game_assets import *
from menu_manipulation import margin, gen_rect, flow_right, below, label_dict_below
from vec2d import *

class StartMenu(Menu):
	highscore = 0
	lastscore = 0	
	
	def __init__(self):
		super(StartMenu,self).__init__()	
		
		max_x = 1366
		max_y = 766
		quarter_y = max_y/4
		quarter_x = max_x/4
		half_x = max_x/2

		title = margin(5,Label(gen_rect(max_x,quarter_y),"PABLOCKY",Color.BLACKGREY,220))
		difficulty_levels = ["easy","medium","hard","impossible"]
		game_modes = ["dodge mode","click mode","groovy mode","circle mode (forbidden)"]	
	
		mode_buttons = label_dict_below(title.rect,{ 
				mode : Button(gen_rect(quarter_x,40), mode, Color.BLUE if mode == "dodge mode" else Color.BLACK, 25)
				for mode in game_modes
		})

		difficulty_buttons = label_dict_below(mode_buttons["dodge mode"].rect,{
					level: Button(gen_rect(quarter_x,40),level, 
					Color.BLUE if level == "easy" else Color.GREY, 25, 
					lambda l=level: self.set_difficulty(l)) 
					for level in difficulty_levels
				})

	
		game_buttons = label_dict_below(difficulty_buttons["easy"].rect,{
					"start": Button(gen_rect(half_x,50),"start", Color.GREEN, 50, self.start_function),
					"quit": Button(gen_rect(half_x,50),"quit",Color.RED, 50, self.quit_function)
		})

		self.labels = {"title" : title}
		self.buttons = difficulty_buttons | game_buttons | mode_buttons
		self.buttons["easy"].set_color(Color.BLUE)

	def process(self):
		pass
	
	def start_function(self):
		MenuManager.mode = "play"
	
	def quit_function(self):
		MenuManager.running = False
		
	def set_difficulty(self, s):
		for key,button in self.buttons.items():
			if key != s and key in ["easy","medium","hard","impossible"]:
				button.set_color(Color.GREY)
		
		self.buttons[s].set_color(Color.BLUE)
		
		difficulty_dict = {
			"easy" : 400,
			"medium": 200,
			"hard": 100,
			"impossible": 50
		}
		if s in difficulty_dict:
			FallerAdder.init_increase_rate = difficulty_dict[s]
			FallerAdder.increase_rate = difficulty_dict[s]
		else:
			FallerAdder.init_increase_rate = difficulty_dict["easy"]
			FallerAdder.increase_rate = difficulty_dict["easy"]

class PlayMenu(Menu):
	def __init__(self):
		super(PlayMenu, self).__init__()
		self.player = Dodger()
		self.score = 0
		self.clock = pygame.time.Clock()
		self.falleradder = FallerAdder()
	
	def handle_events(self):
		super(PlayMenu, self).handle_events()
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				MenuManager.running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE: 
					MenuManager.mode = "menu"
		pressed = pygame.key.get_pressed()
		acceleration = vec2d(0,0)
		if pressed[pygame.K_a]:
			acceleration += vec2d(-1, 0)
		if pressed[pygame.K_d]:
			acceleration += vec2d( 1, 0)	

		if pressed[pygame.K_w]:
			acceleration += vec2d( 0,-1)
		if pressed[pygame.K_s]:
			acceleration += vec2d( 0, 1)

		if pressed[pygame.K_LSHIFT]:
			self.player.friction = 0.5
		else:
			self.player.friction = 0.8

		if acceleration.length > 0:	
			acceleration = 2 * acceleration.normalized()

		self.player.velocity += acceleration	

	def process(self):
		self.falleradder.update()
		self.player.update()				
			
		failed = False	
		
		for faller in Faller._instances.copy():
			faller.update()
			if self.player.get_rect().colliderect(faller.get_rect()):
				failed = True	
			if faller.get_rect().y >= MenuManager.window_height:
				faller.delete()
			
		if failed:
			self.falleradder.reset()	
			MenuManager.mode = "menu"
			self.player.pos = vec2d(400,550)	
		self.clock.tick(60)
	
	def draw(self, screen):	
		super(PlayMenu, self).draw(screen)
		self.player.draw(screen)
		for actor in Actor._instances:
			actor.draw(screen)	
		
class MenuManager(object):
	mode = "menu"
	modes = {"menu" : StartMenu(),"play" : PlayMenu()}
	running = True 
	window_width = 1366
	window_height= 768

	def __init__(self):
		self.screen = pygame.display.set_mode((self.window_width, self.window_height),FULLSCREEN)

	def start(self):
		while MenuManager.running:
			self.handle_events()
			self.process()
			self.update_screen()
	def handle_events(self):
		MenuManager.modes[self.mode].handle_events()
	def process(self):
		MenuManager.modes[self.mode].process()
	def update_screen(self):
		MenuManager.modes[self.mode].draw(self.screen) 
		pygame.display.update()
