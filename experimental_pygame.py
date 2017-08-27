import pygame
import random

class MyGame(object):

    PLAYING, REFRESH, GAME_OVER, WELCOME = range(4)

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.pre_init()
        pygame.init()

        self.width = 800
        self.height = 600
        self.screen = pygame.init()

        self.bg_color = 51, 255, 255

        self.big_font = pygame.font.SysFont(None, 100)
        self.medium_font = pygame.font.SysFont(None, 50)
        self.small_font = pygame.font.SysFont(None, 25)
        # and make the game over text using the big font just loaded
        self.gameover_text = self.big_font.render('GAME OVER', True, (255, 255, 255))

        self.FPS = 30
        pygame.time.set_timer(self.REFRESH, 1000 // self.FPS)

        self.do_welcome()

    def do_welcome(self):
        self.state = MyGame.WELCOME
        self.welcome_mathGame = self.big_font.render("Welcome to this Math Game!", True, (255, 0, 230))
        self.welcome_desc = self.medium_font.render("Click anywhere or press enter to begin", True, (35, 107, 142))



