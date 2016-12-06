"""
Created by pikuldorota

History of modification:
pikuldorota     16 Nov, 2016    Init version
pikuldorota     26 Nov, 2016    Add showing images
pikuldorota      5 Dec, 2016    Change base window settings
pikuldorota      6 Dec, 2016    Create and show Klondike
"""
import pygame
from Card import Card, Suit
from Field import Field
from enum import Enum
from random import shuffle

class Application:
    """Application is main class of the game. It provides base functionality and controls flow of the game."""
    def __init__(self):
        self.deck = []
        pygame.init()
        self.screen = pygame.display.set_mode((495, 450))
        pygame.display.set_icon(pygame.image.load(r"..\images\icon.png"))
        pygame.display.set_caption("Pasjans")
        self.done = False
        self.screen.fill((75, 175, 60))

    def load_deck(self):
        """Loads deck of cards from Ace to King for each out of four suits."""
        for sui in Suit:
            i = 20
            for rank in Enum("rank", "AS,2,3,4,5,6,7,8,9,10,W,D,K"):
                self.deck.append(Card(sui, rank, 20, 20))

    def load_fields(self):
        self.fields = []
        shuffle(self.deck)
        self.fields.append(Field(True, False, False, False, 20, 20))

        self.fields.append(Field(True, True, False, True, 20, 112))
        self.fields.append(Field(True, True, False, True, 83, 112))
        self.fields.append(Field(True, True, False, True, 146, 112))
        self.fields.append(Field(True, True, False, True, 209, 112))
        self.fields.append(Field(True, True, False, True, 272, 112))
        self.fields.append(Field(True, True, False, True, 335, 112))
        self.fields.append(Field(True, True, False, True, 398, 112))

        self.fields.append(Field(False, True, True, False, 209, 20))
        self.fields.append(Field(False, True, True, False, 272, 20))
        self.fields.append(Field(False, True, True, False, 335, 20))
        self.fields.append(Field(False, True, True, False, 398, 20))

        self.fields[0].cards = self.deck[:23]

        self.deck[24].show_hide()
        self.fields[1].cards.append(self.deck[24])

        self.fields[2].cards.append(self.deck[25])
        self.deck[26].show_hide()
        self.fields[2].cards.append(self.deck[26])

        self.fields[3].cards.extend(self.deck[27:29])
        self.deck[29].show_hide()
        self.fields[3].cards.append(self.deck[29])

        self.fields[4].cards.extend(self.deck[30:33])
        self.deck[33].show_hide()
        self.fields[4].cards.append(self.deck[33])

        self.fields[5].cards.extend(self.deck[34:38])
        self.deck[38].show_hide()
        self.fields[5].cards.append(self.deck[38])

        self.fields[6].cards.extend(self.deck[39:44])
        self.deck[44].show_hide()
        self.fields[6].cards.append(self.deck[44])

        self.fields[7].cards.extend(self.deck[45:51])
        self.deck[51].show_hide()
        self.fields[7].cards.append(self.deck[51])

    def execute(self):
        """This is the main game loop function."""
        self.load_deck()
        self.load_fields()
        for field in self.fields:
            field.draw(self.screen)
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
