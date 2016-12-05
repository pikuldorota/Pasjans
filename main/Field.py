"""
Created by pikuldorota

History of modification:
pikuldorota      5 Dec, 2016    Init version
"""
class Field:
    def __init__(self, isPickable, isPuttable, samecolor, descending):
        self.pickable = isPickable
        self.puttable = isPuttable
        self.samecolor = samecolor
        self.descending = descending
        self.cards = []

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
