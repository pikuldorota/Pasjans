"""
Created by pikuldorota

History of modification:
pikuldorota      5 Dec, 2016    Init version
pikuldorota      6 Dec, 2016    Add draw function
pikuldorota     11 Dec, 2016    Refactor to use different classes for
                                different types of fields
pikuldorota     16 Dec, 2016    Add moving multiple cards
pikuldorota     17 Dec, 2016    Add new field: Fours
pikuldorota     28 Dec, 2016    Finished Fours and update clicked
                                function in Field
pikuldorota      7 Jan, 2017    Add index getter and setter for Deck
pikuldorota     12 Jan, 2017    Refactor take method to be more informative
pikuldorota     14 Jan, 2017    Add hiding last card after undoing last move
                                and remove suit field from stack
pikuldorota     27 Jan, 2017    Add subfields and longdeck
pikuldorota     28 Jan, 2017    Add cascade field
pikuldorota     29 Jan, 2017    Add support for undoing moves from subfield
"""
import pygame
from pygame.transform import smoothscale

back = pygame.image.load(r"..\images\back.png")
field = pygame.image.load(r"..\images\rec.png")
k_field = pygame.image.load(r"..\images\krol.png")
as_field = pygame.image.load(r"..\images\as.png")


class Field:
    """This is superclass for all types of fields used in game."""
    def __init__(self, x, y):
        self._cards = []
        self._x = x
        self._y = y

    def hide_last(self):
        """Hides last card on the field"""
        if self._cards:
            self._cards[-1].hide()

    def take(self, cards, revel=False):
        """This method is used to remove specified card from the field"""
        took = False
        for card in cards:
            if card in self._cards:
                self._cards.remove(card)
                took = True
        return took, revel, -1

    def add(self, cards):
        """This method is used to add cards to field when shuffling"""
        if isinstance(cards, list):
            self._cards.extend(cards)
        else:
            self._cards.append(cards)

    def clear(self):
        """Removes all cards from field"""
        self._cards = []

    def show_cards(self):
        """Returns all cards in field"""
        return self._cards

    def clicked(self, x_moved=0, y_moved=0, x_resized=0, y_resized=0):
        """
        Used to determine if field was clicked.
        If multiple cards are chosen, then returns index of clicked one
        """
        mouse_position = pygame.mouse.get_pos()
        rect = pygame.Rect(self._x + x_moved, self._y + y_moved,
                           57 + x_resized * 22, 89 + y_resized * 15)
        if rect.collidepoint(mouse_position):
            if y_resized:
                for i in range(y_resized):
                    rect = pygame.Rect(self._x + x_moved,
                                       self._y + y_moved + i*15, 57, 15)
                    if rect.collidepoint(mouse_position):
                        return i + 1
                return y_resized + 1
            elif x_resized:
                for i in range(x_resized):
                    rect = pygame.Rect(self._x + 35 - i * 22,
                                       self._y + y_moved, 22, 89)
                    if rect.collidepoint(mouse_position):
                        return i + 1
                return x_resized + 1
            else:
                return 1
        return 0


class Deck(Field):
    """This class represents deck field. For details look in documentation"""
    def __init__(self, x, y, vertical=False):
        Field.__init__(self, x, y)
        self.__index = -1

    def get_index(self):
        """Used to return actual index"""
        return self.__index

    def set_index(self, idx):
        """Used to set new index"""
        self.__index = int(idx)

    def update(self, cards):
        """Method used to handle click on the field"""
        if self.clicked():
            if self.__index < len(self._cards) - 1:
                self.__index += 1
                self._cards[self.__index].show()
                return [], self
            else:
                self.__index = -1
                return [], self

        if self.clicked(x_moved=74):
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
            screen.blit(smoothscale(field, (57, 89)), (self._x + 74, self._y))
        else:
            if self.__index == -1:
                screen.blit(smoothscale(field, (57, 89)),
                            (self._x + 74, self._y))
            else:
                self._cards[self.__index].change(self._x + 74, self._y)
                self._cards[self.__index].draw(screen)
            if self.__index == len(self._cards) - 1:
                screen.blit(smoothscale(field, (57, 89)), (self._x, self._y))
            else:
                screen.blit(smoothscale(back, (57, 89)), (self._x, self._y))

    def take(self, card):
        """Removes card from field and changes index to show previous card"""
        took = False
        revel = False
        if len(card) == 1 and card[0] in self._cards:
            self.__index -= 1
            (took, revel, idx) = super().take(card)
        return took, revel, -1

    def add(self, cards):
        """Adds and shows cards to field"""
        if not cards:
            return
        if isinstance(cards, list):
            if len(cards) == 1:
                cards[0].show()
                self.__index+=1
                self._cards.insert(self.__index, cards[0])
            else:
                for card in cards:
                    card.show()
                super().add(cards)
        else:
            cards.show()
            self.__index += 1
            self._cards.insert(self.__index, cards)

    def reset(self):
        """Used when reshuffling to make all cards be covered"""
        self.__index = -1


class Pile(Field):
    """This class represents pile field. For details look in documentation"""
    def __init__(self, x, y, bothway=False, samecolor=False):
        Field.__init__(self, x, y)
        self.__bothway = bothway
        self.__samecolor = samecolor

    def update(self, cards):
        """Used to handle mouse click"""
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
        """Validates putting card on this field and actually puts it"""
        if self._cards and cards[-1] == self._cards[-1]:
            return [], self
        if self._cards:
            if self.__samecolor != self._cards[-1].red_black(cards[0]):
                if self._cards[-1].next_lower(cards[0]) and not self.__bothway:
                    return cards, self
                elif self.__bothway and self._cards[-1].suit() == \
                        cards[-1].suit() and \
                        (self._cards[-1].next_lower(cards[-1])
                            or cards[-1].next_lower(self._cards[-1])):
                    return cards[::-1], self
                else:
                    return [], self
            else:
                return [self._cards[-1]], None
        else:
            if self.__bothway:
                return cards[::-1], self
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

    def take(self, card):
        """Removes asked card from field"""
        (took, revel, idx) = super().take(card)
        if took and self._cards:
            revel = not self._cards[-1].is_shown()
        return took, revel, idx


class Stack(Field):
    """This class represents stack field. For details look in documentation"""
    def __init__(self, x, y, reversed=False):
        Field.__init__(self, x, y)
        self.__reversed = reversed
        if reversed:
            self.__field = k_field
        else:
            self.__field = as_field

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
        """Validate putting card on this field and actually puts it"""
        if len(cards) == 1:
            card = cards[-1]
            if self._cards:
                if card == self._cards[-1]:
                    return [], self
                if self._cards[-1].suit() == card.suit() and \
                    ((card.next_lower(self._cards[-1]) and not self.__reversed) or
                      (self._cards[-1].next_lower(card) and self.__reversed)):
                    card.change(self._x, self._y)
                    return [card], self
                else:
                    return [self._cards[-1]], None
            else:
                if (card.rank().name == "AS" and not self.__reversed) or \
                        (card.rank().name == "K" and self.__reversed):
                    card.change(self._x, self._y)
                    return [card], self
                return [], self
        else:
            if self._cards:
                return [self._cards[-1]], None
            else:
                return [], self

    def draw(self, screen):
        """Used to show cards on the screen"""
        if not self._cards:
            screen.blit(smoothscale(self.__field, (57, 89)), (self._x, self._y))
        else:
            self._cards[-1].change(self._x, self._y)
            self._cards[-1].draw(screen)


class Fours(Field):
    """This class represents fours field. For details look in documentation"""
    def __init__(self, x, y, unputable=False):
        Field.__init__(self, x, y)
        self.__unputable = unputable

    def update(self, cards):
        """Used to handle mouse click"""
        if self._cards:
            idx = self.clicked(x_moved=-(len(self._cards)-1)*22,
                               x_resized=len(self._cards)-1)
        else:
            idx = self.clicked()
        if idx and self._cards and not self._cards[idx-1].is_shown():
            return [], None
        if idx and self._cards and self._cards[idx-1].is_shown() and \
                self.__unputable:
            return self._cards[idx-1:], None
        if idx:
            if cards:
                return self.put(cards)
            else:
                for card in self._cards[idx-1:]:
                    if self._cards[idx-1].rank().name != card.rank().name:
                        return [], None
                return self._cards[idx-1:], None
        return [], None

    def put(self, cards):
        """Validates and puts cards on field"""
        if len(self._cards) + len(cards) > 4:
            return [], self
        if self._cards:
            for card in cards:
                if card.rank().name != self._cards[-1].rank().name:
                    return [], self
            return cards, self
        else:
            for card in cards[1:]:
                if cards[0].rank().name != card.rank().name:
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

    def take(self, cards, revel=False):
        """Takes cards from board and shows the previous one"""
        (took, revel, idx) = super().take(cards)
        if took and self._cards:
            revel = not self._cards[-1].is_shown()
            self._cards[-1].show()
        return took, revel, idx


class Subfield(Field):
    """This class represents subfields for long deck."""
    def draw(self, screen):
        """Used to draw field on the screen"""
        if self._cards:
            self._cards[-1].change(self._x, self._y)
            self._cards[-1].draw(screen)
        else:
            screen.blit(smoothscale(field, (57, 89)), (self._x, self._y))

    def get(self):
        """Used to get last card from field."""
        if self._cards:
            return [self._cards[-1]], None
        return [], self


class LongDeck(Field):
    """This class represents LongDeck. For details look in documentation."""
    def __init__(self, x, y):
        Field.__init__(self, x, y)
        self.__subfields = []
        for i in range(1, 7):
            self.__subfields.append(Subfield(x-i*74, y))

    def draw(self, screen):
        """Used to draw field on the screen"""
        if not self._cards:
            screen.blit(smoothscale(field, (57, 89)), (self._x, self._y))
        else:
            screen.blit(smoothscale(back, (57, 89)), (self._x, self._y))
        for subfield in self.__subfields:
            subfield.draw(screen)

    def add(self, cards):
        """Used to put card on the field"""
        if isinstance(cards, list):
            for i in range(6):
                self.__subfields[i].add(cards[i*4:i*4+4])
            self._cards.extend(cards[24:])
        else:
            self._cards.append(cards)

    def update(self, cards):
        """Used to handle mouse click"""
        if self.clicked():
            if len(self._cards) == 8:
                for i in range(4):
                    self.__subfields[i].add(self._cards[i*2:i*2+2])
                self._cards = []
            else:
                for i in range(6):
                    self.__subfields[i].add(self._cards[i*2:i*2+2])
                self._cards = self._cards[12:]
            return [], self
        for i in range(6):
            if self.clicked(x_moved=-i*74-74):
                return self.__subfields[i].get()
        return [], None

    def take(self, cards, revel=False):
        """Used to remove cards from deck and all the subfields"""
        if len(cards) != 1:
            return False, revel
        if cards[0] in self._cards:
            self._cards.remove(cards[0])
            return True, False
        took = False
        idx = -1
        for subfield in self.__subfields:
            if cards[0] in subfield.show_cards():
                subfield.take(cards)
                took = True
                idx = self.__subfields.index(subfield)
                break
        return took, revel, idx

    def clear(self):
        """Used to clear deck and all the subfields"""
        self._cards = []
        for subfield in self.__subfields:
            subfield.clear()

    def show_subfields(self):
        """Used to read from subfields"""
        return self.__subfields

    def undo(self):
        """Used to undo clicking on deck"""
        if self._cards:
            idx = 6
        else:
            idx = 4
        cards = []
        for subfield in self.__subfields[:idx]:
            card = subfield.get()[0][0]
            subfield.take(subfield.get()[0])
            cards.append(subfield.get()[0][0])
            subfield.take(subfield.get()[0])
            cards.append(card)
        self._cards = cards + self._cards


class UnpickablePile(Pile):
    """This class represents unpickable pile."""
    def update(self, cards):
        """Used to handle mouse click"""
        if self.clicked(y_moved=15*len(self._cards[:-1])):
            return [self._cards[-1]], None
        return [], None


class Cascade(Fours):
    """Represents cascade field"""
    def __init__(self, x, y, previous=None):
        Fours.__init__(self, x, y)
        self.__previous = previous

    def update(self, cards):
        """Used to handle mouse click"""
        if self.clicked(x_resized=len(self._cards[:-1]),
                        x_moved=-22*len(self._cards[:-1])):
            if not cards:
                return [], self
            if self.__previous:
                prev_cards = self.__previous.show_cards()
                if next((card for card in prev_cards
                        if card.rank().name == cards[0].rank().name), None):
                    return cards, self
                else:
                    return [], None
            else:
                if self._cards and self._cards[0].suit().name == \
                  cards[0].suit().name:
                    return cards, self
                elif not self._cards:
                    return cards, self
                else:
                    return [], None
        else:
            return [], None
