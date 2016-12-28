"""
Created by pikuldorota

History of modification:
pikuldorota     16 Nov, 2016    Init version
pikuldorota     26 Nov, 2016    Add showing images
pikuldorota      5 Dec, 2016    Change base window settings
pikuldorota      6 Dec, 2016    Create and show Klondike
pikuldorota     11 Dec, 2016    Change handling of mouse click
pikuldorota     16 Dec, 2016    Add moving multiply cards
pikuldorota     17 Dec, 2016    Add beta menu
"""
import pygame
from Card import Card, Suit
import Board
from enum import Enum


class Application:
    """Application is main class of the game. It provides base functionality and controls flow of the game."""
    def __init__(self):
        self.__deck = []
        pygame.init()
        self.__screen = pygame.display.set_mode((475, 510))
        self.__new_game = pygame.image.load("../images/newgame.png")
        self.__change_game = pygame.image.load("../images/changegame.png")
        self.__undo = pygame.image.load("../images/undo.png")
        pygame.display.set_icon(pygame.image.load(r"..\images\icon.png"))
        pygame.display.set_caption("Patience")
        self.__done = False
        self.__board = []
        self.__activeCard = []
        self.__field = None
        self.__chosen_play = "klondike"

    def load_deck(self):
        """Loads deck of cards from Ace to King for each out of four suits."""
        for sui in Suit:
            for rank in Enum("rank", "AS,2,3,4,5,6,7,8,9,10,W,D,K"):
                self.__deck.append(Card(sui, rank, 20, 20))

    def load_fields(self, chosen_play):
        """Loads chosen board"""
        self.__chosen_play = chosen_play
        self.__activeCard = []
        for card in self.__deck:
            card.hide()
        self.__board = getattr(Board, chosen_play)(self.__deck)

    def remove_from_fields(self, card):
        """Used to clear board from cards"""
        for field in self.__board:
            if field.take(card):
                break

    def redraw(self):
        """Used after each move to actualize game on the screen"""
        self.__screen.fill((75, 175, 60))
        for field in self.__board:
            field.draw(self.__screen)
        self.__screen.blit(self.__new_game, (5, 0))
        self.__screen.blit(self.__change_game, (119, 0))
        self.__screen.blit(self.__undo, (250, 0))
        pygame.display.update()

    def check_cards(self):
        """To do: check for fields being clicked should be here"""
        pass

    def check_menu(self):
        """Determines if one of buttons where clicked. If one was then proceed with action"""
        rect = pygame.Rect(5, 0, 109, 33)
        mouse_position = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_position):
            for card in self.__deck:
                card.hide()
            self.__activeCard = []
            self.__board = getattr(Board, self.__chosen_play + "_shuffle")(self.__board, self.__deck)
            return True

        rect = pygame.Rect(119, 0, 126, 33)
        if rect.collidepoint(mouse_position):
            self.load_fields("fifteen_puzzle")
            self.__activeCard = []
            return True

        return False

    def execute(self):
        """This is the main game loop function."""
        self.load_deck()
        self.load_fields("fifteen_puzzle")
        self.redraw()
        while not self.__done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.check_menu():
                        change = False
                        for field in self.__board:
                            (cards, fiel) = field.update(self.__activeCard)
                            if cards:
                                if fiel is not None:
                                    for pole in self.__board:
                                        pole.take(cards)
                                    fiel.add(cards)
                                    self.__activeCard = []
                                else:
                                    self.__activeCard = cards
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
                        for card in self.__deck:
                            card.change_active(False)
                        for card in self.__activeCard:
                            card.change_active(True)
                    self.redraw()
            pygame.display.flip()

if __name__ == "__main__":
    theApp = Application()
    theApp.execute()
