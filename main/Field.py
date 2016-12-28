"""
Created by pikuldorota

History of modification:
pikuldorota      5 Dec, 2016    Init version
pikuldorota      6 Dec, 2016    Add draw function
pikuldorota     11 Dec, 2016    Refactor to use different classes for different types of fields
pikuldorota     17 Dec, 2016    Add moving multiple cards
pikuldorota     17 Dec, 2016    Add new field: Fours
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

    def clear(self):
        """Removes all cards from field"""
        self._cards = []

    def clicked(self, x_moved=0, y_moved=0, x_resized=0, y_resized=0):
        """Used to determine if field was clicked. If multiple cards are chosen, then returns index of clicked one"""
        mouse_position = pygame.mouse.get_pos()
        rect = pygame.Rect(self._x + x_moved, self._y + y_moved, 57 + x_resized * 22, 89 + y_resized * 15)
        if rect.collidepoint(mouse_position):
            if y_resized:
                for i in range(y_resized):
                    rect = pygame.Rect(self._x + x_moved, self._y + y_moved + i*15, 57, 15)
                    if rect.collidepoint(mouse_position):
                        return i + 1
                return y_resized + 1
            elif x_resized:
                for i in range(x_resized):
                    rect = pygame.Rect(self._x + 35 - i * 22, self._y + y_moved, 22, 89)
                    if rect.collidepoint(mouse_position):
                        return i + 1
                return x_resized + 1
            else:
                return 1
        return 0


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

        if self.clicked(x_moved=63):
            if cards and self._cards[self.__index] == cards[-1]:
                if self._cards[self.__index].is_active():
                    return [self._cards[self.__index]], None
            else:
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
        """It removes asked card from field and changes index to show previous card"""
        if len(card) == 1 and card[0] in self._cards:
            self.__index -= 1
            super().take(card)

    def add(self, cards):
        """Adds and shows cards to field"""
        super().add(cards)
        for card in cards:
            card.show()

    def reset(self):
        """Used when reshuffling to make all cards be covered"""
        self.__index = -1


class Pile(Field):
    """Field representing piles where cards are being put one on another in descending order and alternately colors"""
    def update(self, cards):
        """Used to handle muse click"""
        i = 0
        for (idx, each) in enumerate(self._cards):
            if each.is_shown():
                i = idx
                break
        if self._cards:
            resized = len(self._cards) - i - 1
        else:
            resized = 0
        idx = self.clicked(y_moved=i * 15, y_resized=resized)
        if idx:
            if cards:
                return self.put(cards)
            else:
                if self._cards:
                    return self._cards[idx-1+i:], None
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
    """Field representing one where player puts cards from ace to king in ascending order, all in the same suit"""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.__suit = None

    def update(self, cards):
        """Used to handle mouse click"""
        if self.clicked():
            if cards:
                return self.put(cards)
            else:
                if self._cards:
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
                if self.__suit == card.suit() and card.next_lower(self._cards[-1]):
                    card.change(self._x, self._y)
                    return [card], self
                else:
                    return [self._cards[-1]], None
            else:
                if card.rank().name == "AS":
                    card.change(self._x, self._y)
                    self.__suit = card.suit()
                    return [card], self
                return [], self
        else:
            return [self._cards[-1]], None

    def draw(self, screen):
        """Used to show cards on the screen"""
        if not self._cards:
            screen.blit(smoothscale(field, (57, 89)), (self._x, self._y))
        else:
            self._cards[-1].draw(screen)


class Fours(Field):
    """Field representing one where at most can be four cards. One is put on another only if has the same rank"""
    def update(self, cards):
        idx = self.clicked(x_moved=-(len(self._cards)-1)*22, x_resized=len(self._cards)-1)
        if idx:
            if cards:
                return self.put(cards)
            else:
                for card in self._cards[idx:]:
                    if self._cards[idx].rank() != card.rank():
                        return [], None
                return self._cards[idx-1:], None
        return [], None

    def put(self, cards):
        if len(self._cards) + len(cards) > 4:
            return [], self
        if self._cards:
            for card in cards:
                if card.rank() != self._cards[-1].rank():
                    return [], self
            return cards, self
        else:
            for card in cards[1:]:
                if cards[0].rank() != card.rank():
                    return [], self
            return cards, self

    def draw(self, screen):
        """Used to show cards on the screen"""
        if not self._cards:
            screen.blit(smoothscale(field, (57, 89)), (self._x, self._y))
        else:
            i = 0
            for card in self._cards:
                card.change(self._x - i * 22, self._y)
                card.draw(screen)
                i += 1
