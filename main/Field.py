"""
Created by pikuldorota

History of modification:
pikuldorota      5 Dec, 2016    Init version
pikuldorota      6 Dec, 2016    Add draw function
pikuldorota     11 Dec, 2016    Refactor to use different classes for different types of fields
"""
import pygame
from pygame.transform import smoothscale

back = pygame.image.load(r"..\images\back.png")
field = pygame.image.load(r"..\images\rec.png")


class Field:
    """This is superclass for all types of fields used in game."""
    def __init__(self, x, y):
        self._cards = []
        self._x = x
        self._y = y

    def take(self, card):
        """This method is used to remove specified card from the field"""
        if card in self._cards:
            self._cards.remove(card)

    def add(self, cards):
        """This method is used to add cards to field at the beginning of game"""
        if isinstance(cards, list):
            self._cards.extend(cards)
        else:
            self._cards.append(cards)


class Deck(Field):
    """This class represents deck field. The one where player can click through the cards to choose one of them"""
    def __init__(self, x, y):
        Field.__init__(self, x, y)
        self.__index = -1

    def update(self, card):
        """Method used to handle click on the field"""
        mouse_position = pygame.mouse.get_pos()
        rect = pygame.Rect(self._x, self._y, 57, 89)
        if rect.collidepoint(mouse_position):
            if self.__index < len(self._cards)-1:
                self.__index += 1
                self._cards[self.__index].show()
            else:
                self.__index = -1
            if card:
                card.change_active(False)

        rect = pygame.Rect(self._x + 63, self._y, 57, 89)
        if rect.collidepoint(mouse_position):
            if self._cards[self.__index] == card:
                self._cards[self.__index].change_active(opposite=True)
                if self._cards[self.__index].is_active():
                    return self._cards[self.__index]
            else:
                self._cards[self.__index].change_active(True)
                if card:
                    card.change_active(False)
                return self._cards[self.__index]

    def draw(self, screen):
        """Method used to show deck on the screen"""
        if not self._cards:
            screen.blit(smoothscale(field, (57, 89)), (self._x, self._y))
            screen.blit(smoothscale(field, (57, 89)), (self._x + 63, self._y))
        else:
            if self.__index == -1:
                screen.blit(smoothscale(field, (57, 89)), (self._x + 63, self._y))
            else:
                self._cards[self.__index].change(self._x + 63, self._y)
                self._cards[self.__index].draw(screen)
            if self.__index == len(self._cards) - 1:
                screen.blit(smoothscale(field, (57, 89)), (self._x, self._y))
            else:
                screen.blit(smoothscale(back, (57, 89)), (self._x, self._y))


class Pile(Field):
    """Field representing piles where cards are being put one on another in descending order and alternately colors"""
    def update(self, card):
        """Used to handle muse click"""
        if card:
            card.change_active(False)
        self._cards[-1].update()
        if self._cards[-1].is_active():
            return self._cards[-1]

    def put(self, card):
        """Used to validate putting card on this field and actually putting it"""
        pass

    def draw(self, screen):
        """Used to show cards on the screen"""
        if not self._cards:
            screen.blit(smoothscale(field, (57, 89)), (self._x, self._y))
        else:
            i = 0
            for card in self._cards:
                card.change(self._x, self._y + i)
                i += 15
                card.draw(screen)


class Stack(Field):
    def update(self, card):
        """Used to handle mouse click"""
        if card:
            card.change_active(False)

    def put(self, card):
        """Used to validate putting card on this field and actually putting it"""
        pass

    def draw(self, screen):
        """Used to show cards on the screen"""
        if not self._cards:
            screen.blit(smoothscale(field, (57, 89)), (self._x, self._y))
        else:
            self._cards[-1].draw(screen)
