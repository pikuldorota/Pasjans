"""
Created by pikuldorota

History of modification:
pikuldorota     16 Nov, 2016    Init version
pikuldorota     26 Nov, 2016    Add showing images
pikuldorota      5 Dec, 2016    Change base window settings
pikuldorota      6 Dec, 2016    Create and show Klondike
pikuldorota     11 Dec, 2016    Change handling of mouse click
"""
import pygame
from Card import Card, Suit
import Board
from enum import Enum
from random import shuffle


class Application:
    """Application is main class of the game. It provides base functionality and controls flow of the game."""
    def __init__(self):
        self.__deck = []
        pygame.init()
        self.__screen = pygame.display.set_mode((475, 450))
        pygame.display.set_icon(pygame.image.load(r"..\images\icon.png"))
        pygame.display.set_caption("Pasjans")
        self.__done = False
        self.__screen.fill((75, 175, 60))
        self.__board = []
        self.__activeCard = []
        self.__field = None

    def load_deck(self):
        """Loads deck of cards from Ace to King for each out of four suits."""
        for sui in Suit:
            for rank in Enum("rank", "AS,2,3,4,5,6,7,8,9,10,W,D,K"):
                self.__deck.append(Card(sui, rank, 20, 20))

    def load_fields(self, choosenPlay):
        """Loads choosen board"""
        shuffle(self.__deck)
        for card in self.__deck:
            card.hide()
        self.__board = getattr(Board, choosenPlay)(self.__deck)

    def remove_from_fields(self, card):
        for field in self.__board:
            if field.take(card):
                break

    def execute(self):
        """This is the main game loop function."""
        self.load_deck()
        self.load_fields("klondike")
        for field in self.__board:
            field.draw(self.__screen)
        while not self.__done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    change = False
                    for field in self.__board:
                        (card, fiel) = field.update(self.__activeCard)
                        if card:
                            if fiel is not None:
                                for pole in self.__board:
                                    pole.take(card)
                                fiel.add(card)
                                self.__activeCard = []
                            else:
                                self.__activeCard = card
                            change = True
                            break
                        else:
                            if fiel is not None:
                                change = True
                                self.__activeCard = []
                                break

                    if not change:
                        if self.__activeCard:
                            for card in self.__activeCard:
                                card.change_active(False)
                        self.__activeCard = []

                    self.__screen.fill((75, 175, 60))
                    for field in self.__board:
                        field.draw(self.__screen)
                    pygame.display.update()
            pygame.display.flip()

if __name__ == "__main__":
    theApp = Application()
    theApp.execute()
