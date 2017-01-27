"""
Created by pikuldorota

History of modification:
pikuldorota     16 Nov, 2016    Init version
pikuldorota     26 Nov, 2016    Add card coordinates
pikuldorota      5 Dec, 2016    Change reaction to move
pikuldorota      6 Dec, 2016    Add option to show both front and back
                                of the card
pikuldorota     11 Dec, 2016    Refactor it to make all class fields private,
                                getters and setters created for them
pikuldorota     16 Dec, 2016    Add useful getters and methods to compare cards
pikuldorota     17 Dec, 2016    Replace is_AS function with more useful
                                rank function
pikuldorota      7 Jan, 2017    Add is_xml_card function
pikuldorota     27 Jan, 2017    Adapt to maximum line length from PEP 8
"""
import pygame
from enum import Enum
from pygame.transform import smoothscale
from Field import back


class Suit(Enum):
    """It shows suits for cards and also their colours."""
    pik = "black"
    trefl = "BLACK"
    karo = "red"
    kier = "RED"


class Card(pygame.sprite.Sprite):
    """Class for representing each card"""
    def __init__(self, sui, rank, x, y):
        self.__suit = sui
        self.__rank = rank
        self.__front = pygame.image.load("..\images\{0}_{1}.png"
                                         .format(rank.name, sui.name))
        self.__x = x
        self.__y = y
        self.__isActive = False
        self.__isShown = False

    def draw(self, screen):
        """Show card on the screen"""
        if self.__isActive:
            pygame.draw.rect(screen, (245, 245, 245), (self.__x - 2, self.__y - 2, 61, 93))  # (205,133,63)
        if self.__isShown:
            screen.blit(smoothscale(self.__front, (57, 89)), (self.__x, self.__y))
        else:
            screen.blit(smoothscale(back, (57, 89)), (self.__x, self.__y))

    def change(self, x, y):
        """Changes card positions"""
        self.__x = x
        self.__y = y

    def show(self):
        """Method to make card visible"""
        self.__isShown = True

    def hide(self):
        """Method to hide card"""
        self.__isShown = False

    def change_active(self, is_active=False):
        """Used when card is click to change it's active field"""
        self.__isActive = is_active

    def is_active(self):
        """Returns true when card is chosen to be used and false otherwise"""
        return self.__isActive

    def is_shown(self):
        """Returns true if card is shown"""
        return self.__isShown

    def red_black(self, card):
        """Returns true if one card is red and another one is black"""
        return self.__suit.value.lower() != card.__suit.value.lower()

    def next_lower(self, card):
        """Returns true if asked card is lower by rank than self one"""
        return self.__rank.value == card.__rank.value + 1

    def suit(self):
        """Returns suit of card"""
        return self.__suit

    def rank(self):
        """Returns rank of card"""
        return self.__rank

    def is_xml_card(self, card_xml):
        """Checks if xml node describes this card"""
        if self.__rank.name != card_xml.getAttribute("rank"):
            return False
        if self.__suit.name != card_xml.getAttribute("suit"):
            return False
        return True
