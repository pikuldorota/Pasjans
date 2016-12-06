"""
Created by pikuldorota

History of modification:
pikuldorota      5 Dec, 2016    Init version
pikuldorota      6 Dec, 2016    Add draw function
"""
import pygame
from pygame.transform import smoothscale

back = pygame.image.load(r"..\images\back.png")
field = pygame.image.load(r"..\images\rec.png")

class Field:
    def __init__(self, isPickable, isPuttable, samecolor, descending, x, y):
        self.pickable = isPickable
        self.puttable = isPuttable
        self.samecolor = samecolor
        self.descending = descending
        self.cards = []
        self.x = x
        self.y = y
        self.index = -1  # used only in talia to tell which one is shown

    def draw(self, screen):
        if not self.cards:
            screen.blit(smoothscale(field, (57, 89)), (self.x, self.y))
            if self.pickable and not self.puttable:  # talia
                screen.blit(smoothscale(field, (57, 89)), (self.x + 63, self.y))
        else:
            if self.pickable and self.puttable:
                i = 0
                for card in self.cards:
                    card.change(self.x, self.y + i)
                    i += 20
                    card.draw(screen)
            elif not self.pickable and self.puttable:
                self.cards[-1].draw(screen)
            elif self.pickable and not self.puttable:
                if self.index == -1:
                    screen.blit(smoothscale(field, (57, 89)), (self.x + 63, self.y))
                else:
                    self.cards[self.index].change(self.x + 60, self.y)
                    self.cards[self.index].draw()
                if self.index == len(self.cards):
                    screen.blit(smoothscale(field, (57, 89)), (self.x, self.y))
                else:
                    screen.blit(smoothscale(back, (57, 89)), (self.x, self.y))


    def put(self, card):
        """Puts card on the field depending on validaton result. Returns True if move was valid and False otherwise"""
        if not self.puttable:
            return False
        if not self.cards:
            if self.descending:
                self.cards.append(card)
                return True
            else:
                if card.rank.name == "AS":
                    self.cards.append(card)
                    return True
                return False
        if (self.cards[-1].suit.name.lower() == card.suit.lower()) == self.samecolor:
            pass
