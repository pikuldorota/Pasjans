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

    def take(self, cards):
        """This method is used to remove specified card from the field"""
        for card in cards:
            if card in self._cards:
                self._cards.remove(card)

    def add(self, cards):
        """This method is used to add cards to field at the beginning of game"""
        if isinstance(cards, list):
            self._cards.extend(cards)
        else:
            self._cards.append(cards)

    def clicked(self, x_moved=0, y_moved=0, x_resized=0, y_resized=0):
        mouse_position = pygame.mouse.get_pos()
        rect = pygame.Rect(self._x + x_moved, self._y + y_moved, 57 + x_resized, 89 + y_resized)
        if rect.collidepoint(mouse_position):
            return True
        return False


class Deck(Field):
    """This class represents deck field. The one where player can click through the cards to choose one of them"""
    def __init__(self, x, y):
        Field.__init__(self, x, y)
        self.__index = -1

    def update(self, cards):
        """Method used to handle click on the field"""
        if self.clicked():
            if self.__index < len(self._cards) - 1:
                self.__index += 1
                self._cards[self.__index].show()
            else:
                self.__index = -1
            if cards:
                for card in cards:
                    card.change_active(False)

        if self.clicked(x_moved=63):
            if cards and self._cards[self.__index] == cards[-1]:
                self._cards[self.__index].change_active(opposite=True)
                if self._cards[self.__index].is_active():
                    return [self._cards[self.__index]], None
            else:
                self._cards[self.__index].change_active(True)
                if cards:
                    for card in cards:
                        card.change_active(False)
                return [self._cards[self.__index]], None
        return [], None

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

    def take(self, card):
        if len(card) == 1 and card[0] in self._cards:
            self.__index -= 1
            super().take(card)

    def add(self, cards):
        super().add(cards)
        for card in cards:
            card.show()


class Pile(Field):
    """Field representing piles where cards are being put one on another in descending order and alternately colors"""
    def update(self, cards):
        """Used to handle muse click"""
        i = 0
        for (idx, each) in enumerate(self._cards):
            if each.is_shown():
                i = idx
                break
        if self.clicked(y_moved=i * 15, y_resized=(len(self._cards) - i - 1) * 15):
            if cards:
                for card in cards:
                    card.change_active(False)
                return self.put(cards)
            else:
                if self._cards:
                    for idx in range(i, len(self._cards)):
                        self._cards[i].change_active(True)
                    return self._cards[i:], None
                return [], self
        return [], None

    def put(self, cards):
        """Used to validate putting card on this field and actually putting it"""
        if self._cards and cards[-1] == self._cards[-1]:
            return [], self
        if self._cards:
            if self._cards[-1].red_black(cards[0]) and self._cards[-1].next_lower(cards[0]):
                return cards, self
            else:
                self._cards[-1].change_active(True)
                return [self._cards[-1]], None
        else:
            return cards, self

    def draw(self, screen):
        """Used to show cards on the screen"""
        if not self._cards:
            screen.blit(smoothscale(field, (57, 89)), (self._x, self._y))
        else:
            if self._cards:
                self._cards[-1].show()
            i = 0
            for card in self._cards:
                card.change(self._x, self._y + i)
                i += 15
                card.draw(screen)


class Stack(Field):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.__color = None

    def update(self, cards):
        """Used to handle mouse click"""
        if self.clicked():
            if cards:
                for card in cards:
                    card.change_active(False)
                return self.put(cards)
            else:
                if self._cards:
                    self._cards[-1].change_active(True)
                    return [self._cards[-1]], None
                return [], self
        return [], None

    def put(self, cards):
        """Used to validate putting card on this field and actually putting it"""
        if len(cards) == 1:
            card = cards[-1]
            if self._cards:
                if card == self._cards[-1]:
                    return [], self
                if self.__color == card.color() and card.next_lower(self._cards[-1]):
                    card.change(self._x, self._y)
                    return [card], self
                else:
                    self._cards[-1].change_active(True)
                    return [self._cards[-1]], None
            else:
                if card.is_AS():
                    card.change(self._x, self._y)
                    self.__color = card.color()
                    return [card], self
                return [], self
        else:
            self._cards[-1].change_active(True)
            return [self._cards[-1]], None

    def draw(self, screen):
        """Used to show cards on the screen"""
        if not self._cards:
            screen.blit(smoothscale(field, (57, 89)), (self._x, self._y))
        else:
            self._cards[-1].draw(screen)
