"""
Created by pikuldorota

History of modification:
pikuldorota     16 Nov, 2016    Init version
pikuldorota     26 Nov, 2016    Add card coordinates
pikuldorota      5 Dec, 2016    Change reaction to move
pikuldorota      6 Dec, 2016    Add option to show both front and back of the card
"""
import pygame
from enum import Enum
from pygame.transform import smoothscale
from Field import back
from pygame.locals import *


class Suit(Enum):
    """It shows suits for cards and also their colours. They are in sequence spades, clubs, diamonds, hearts"""
    pik = "black"
    trefl = "BLACK"
    karo = "red"
    kier = "RED"


class Card(pygame.sprite.Sprite):
    """Class for representing each card"""
    def __init__(self, sui, rank, x, y):
        self.suit = sui
        self.rank = rank
        self.front = pygame.image.load("..\images\{0}_{1}.png".format(rank.name, sui.name))
        self.x = x
        self.y = y
        self.isactive = False
        self.isShown = False

    def update(self):
        """Changes position after move"""
        mpos = pygame.mouse.get_pos()
        rect = self.front.get_rect()
        if rect.collidepoint(mpos):
            self.isactive = True

    def draw(self, screen):
        """Show card on the screen"""
        if self.isactive:
            pygame.draw.rect(screen, (245, 245, 245), (self.x-2, self.y-2, 61, 93))  # (205,133,63)
        if self.isShown:
            screen.blit(smoothscale(self.front, (57, 89)), (self.x, self.y))
        else:
            screen.blit(smoothscale(back, (57, 89)), (self.x, self.y))

    def change(self, x, y):
        """Changes card positions"""
        self.x = x
        self.y = y

    def show_hide(self):
        self.isShown = not self.isShown
