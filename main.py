#!/usr/bin python3
import pygame
import pygame.mixer as mixer

from game_menus import MenuManager

pygame.init()
mixer.init()
 
s = mixer.Sound("background.ogg")
c = mixer.Channel(1)

c.play(s,loops=-1, fade_ms=100)

game = MenuManager()
game.start()
