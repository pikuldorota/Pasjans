import pygame
from Card import Card, Suit
from enum import Enum
from random import shuffle
from pygame.locals import *


class Application:
    def __init__(self):
        self.deck = []
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        self.done = False
        self.screen.fill((75, 175, 60))

    def load_deck(self):
        for sui in Suit:
            for rank in Enum("rank", "AS,2,3,4,5,6,7,8,9,10,W,D,K"):
                self.deck.append(Card(sui, rank))
        shuffle(self.deck)

    def execute(self):
        self.load_deck()
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
            pygame.display.flip()

if __name__ == "__main__":
    theApp = Application()
    theApp.execute()
