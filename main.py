#!/usr/bin python3
import pygame
from game_menus import MenuManager

pygame.init()

s = pygame.mixer.Sound("background.ogg")
c = pygame.mixer.Channel(1)

c.play(s,loops=-1, fade_ms=100)

game = MenuManager()
game.start()
