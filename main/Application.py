"""
Created by pikuldorota

History of modification:
pikuldorota     16 Nov, 2016    Init version
pikuldorota     26 Nov, 2016    Add showing images
pikuldorota      5 Dec, 2016    Change base window settings
"""
import pygame
from Card import Card, Suit
from enum import Enum
from random import shuffle
from pygame.transform import smoothscale
from pygame.locals import *


class Application:
    """Application is main class of the game. It provides base functionality and controls flow of the game."""
    def __init__(self):
        self.deck = []
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 500))
        pygame.display.set_icon(pygame.image.load(r"..\images\icon.png"))
        pygame.display.set_caption("Pasjans")
        self.back = pygame.image.load(r"..\images\back.png")
        self.done = False
        self.screen.fill((75, 175, 60))

    def load_deck(self):
        """Loads deck of cards from Ace to King for each out of four suits."""
        for sui in Suit:
            i = 20
            for rank in Enum("rank", "AS,2,3,4,5,6,7,8,9,10,W,D,K"):
                self.deck.append(Card(sui, rank, 20, 20))
        shuffle(self.deck)
        for card in self.deck:
            card.change(i, 20)
            card.draw(self.screen)
            i+=10

    def execute(self):
        """This is the main game loop function."""
        self.load_deck()
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for card in self.deck:
                        card.update()
                    self.screen.fill((75, 175, 60))
                    for card in self.deck:
                        card.draw(self.screen)
                    pygame.display.update()
            pygame.display.flip()

if __name__ == "__main__":
    theApp = Application()
    theApp.execute()
