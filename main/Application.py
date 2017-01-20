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
pikuldorota     28 Dec, 2016    Clean activeCard field when loading new game or shuffling cards
pikuldorota      7 Jan, 2017    Refactor change game option and add autosave
pikuldorota     12 Jan, 2017    Add saving moves
pikuldorota     14 Jan, 2017    Add undo functionality to menu
pikuldorota     20 Jan, 2017    Add new menu options
"""
import xml.dom.minidom as minidom
from enum import Enum

import pygame

import Board
from Card import Card, Suit
from XMLutils import *


class Application:
    """Application is main class of the game. It provides base functionality and controls flow of the game."""
    def __init__(self):
        self.__deck = []
        pygame.init()
        self.__screen = pygame.display.set_mode((540, 580))
        self.__new_game = pygame.image.load("../images/newgame.png")
        self.__change_game = pygame.image.load("../images/changegame.png")
        self.__undo = pygame.image.load("../images/undo.png")
        self.__canfield = pygame.image.load("../images/canfield.png")
        self.__clock = pygame.image.load("../images/clock.png")
        self.__fifteen_puzzle = pygame.image.load("../images/fifteen_puzzle.png")
        self.__klondike = pygame.image.load("../images/klondike.png")
        self.__algiernian = pygame.image.load("../images/algiernian.png")
        self.__osmosis = pygame.image.load("../images/osmosis.png")
        pygame.display.set_icon(pygame.image.load(r"../images/icon.png"))
        pygame.display.set_caption("Patience")
        self.__done = False
        self.__board = []
        self.__activeCard = []
        self.__chosen_play = ""
        self.__to_be_changed = False
        self.__ranks = Enum("rank", "AS,2,3,4,5,6,7,8,9,10,W,D,K")
        self.__saved = None

    def load_deck(self):
        """Loads deck of cards from Ace to King for each out of four suits."""
        for sui in Suit:
            for rank in self.__ranks:
                self.__deck.append(Card(sui, rank, 20, 20))

    def load_fields(self, chosen_play):
        """Loads chosen board"""
        if self.__saved:
            game_state_to_xml(self.__board, self.__saved)
            with open("../save_files/{}.xml".format(self.__chosen_play), 'w') as f:
                self.__saved.writexml(f)
        self.__chosen_play = chosen_play
        self.__activeCard = []
        for card in self.__deck:
            card.hide()
        if chosen_play == "clock":
            self.__board = getattr(Board, chosen_play)(self.__deck, self.__ranks)
        else:
            self.__board = getattr(Board, chosen_play)(self.__deck)
        self.__saved = minidom.parse("../save_files/{}.xml".format(chosen_play))
        latest = self.__saved.getElementsByTagName("LatestCardPositions")[0]
        if len(latest.getElementsByTagName("Field")):
            game_state_from_xml(self.__board, self.__deck, self.__saved)

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
        if self.__to_be_changed:
            self.__screen.blit(self.__algiernian, (4, 1))
            self.__screen.blit(self.__canfield, (95, 1))
            self.__screen.blit(self.__clock, (182, 1))
            self.__screen.blit(self.__fifteen_puzzle, (254, 1))
            self.__screen.blit(self.__klondike, (371, 1))
            self.__screen.blit(self.__osmosis, (460, 1))
        else:
            self.__screen.blit(self.__new_game, (5, 0))
            self.__screen.blit(self.__change_game, (119, 0))
            self.__screen.blit(self.__undo, (250, 0))
        pygame.display.update()

    def check_cards(self):
        """Check if click occured on any card and performs update"""
        for field in self.__board:
            (cards, fiel) = field.update(self.__activeCard)
            if cards:
                if fiel is not None:
                    for i, pole in enumerate(self.__board):
                        (took, reveled) = pole.take(cards)
                        if took:
                            break
                    fiel.add(cards)
                    add_move_to_xml(i, self.__board.index(fiel), cards, reveled, self.__saved)
                    self.__activeCard = []
                else:
                    self.__activeCard = cards
                return True
            else:
                if fiel is not None:
                    if isinstance(fiel, Deck):
                        add_move_to_xml(self.__board.index(fiel), self.__board.index(fiel),
                                        [], False, self.__saved)
                    self.__activeCard = []
                    return True
        return False

    def check_menu(self):
        """Determines if one of buttons where clicked. If one was then proceed with action"""
        mouse_position = pygame.mouse.get_pos()
        if self.__to_be_changed:
            rect = pygame.Rect(4, 1, 88, 33)
            if rect.collidepoint(mouse_position):
                self.load_fields("algiernian")
                self.__to_be_changed = False
                return True

            rect = pygame.Rect(95, 1, 82, 33)
            if rect.collidepoint(mouse_position):
                self.load_fields("canfield")
                self.__to_be_changed = False
                return True

            rect = pygame.Rect(182, 1, 67, 33)
            if rect.collidepoint(mouse_position):
                self.load_fields("clock")
                self.__to_be_changed = False
                return True

            rect = pygame.Rect(254, 1, 112, 33)
            if rect.collidepoint(mouse_position):
                self.load_fields("fifteen_puzzle")
                self.__to_be_changed = False
                return True

            rect = pygame.Rect(371, 1, 84, 33)
            if rect.collidepoint(mouse_position):
                self.load_fields("klondike")
                self.__to_be_changed = False
                return True

            rect = pygame.Rect(460, 1, 77, 33)
            if rect.collidepoint(mouse_position):
                self.load_fields("osmosis")
                self.__to_be_changed = False
                return True
        else:
            "New game"
            rect = pygame.Rect(5, 0, 109, 33)
            if rect.collidepoint(mouse_position):
                clean_moves_xml(self.__saved)
                for card in self.__deck:
                    card.hide()
                self.__activeCard = []
                self.__board = getattr(Board, self.__chosen_play + "_shuffle")(self.__board, self.__deck)
                return True

            "Change game"
            rect = pygame.Rect(119, 0, 126, 33)
            if rect.collidepoint(mouse_position):
                self.__to_be_changed = True
                self.__activeCard = []
                return True

            "Undo"
            rect = pygame.Rect(250, 0, 76, 33)
            if rect.collidepoint(mouse_position):
                undo_last_move(self.__board, self.__deck, self.__saved)
                self.__activeCard = []
                return True
        return False

    def check_is_finished(self):
        """After each move checks if patience has been solved"""
        check = getattr(Board, self.__chosen_play + "_is_finished")(self.__board)
        if check:
            myfont = pygame.font.SysFont("sans-serif", 40)
            label = myfont.render("Congratulations!", 1, (255, 255, 255))
            self.__screen.blit(label, (110, 200))

    def execute(self):
        """This is the main game loop function."""
        self.load_deck()
        with open("../save_files/last", 'r+') as f:
            content = f.read()
            if content:
                self.__chosen_play = content
                self.load_fields(content)
            else:
                self.load_fields("klondike")
        self.redraw()
        while not self.__done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.check_menu():
                        if not self.check_cards():
                            if self.__activeCard:
                                for card in self.__activeCard:
                                    card.change_active(False)
                            self.__activeCard = []
                        for card in self.__deck:
                            card.change_active(False)
                        for card in self.__activeCard:
                            card.change_active(True)
                        self.__to_be_changed = False
                    self.redraw()
                    self.check_is_finished()
            pygame.display.flip()
        with open("../save_files/last", 'w') as f:
            f.write(self.__chosen_play)
        if self.__saved:
            game_state_to_xml(self.__board, self.__saved)
            with open("../save_files/{}.xml".format(self.__chosen_play), 'w') as f:
                self.__saved.writexml(f)


if __name__ == "__main__":
    theApp = Application()
    theApp.execute()
