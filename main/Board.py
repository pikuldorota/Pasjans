"""
Created by pikuldorota

History of modification:
pikuldorota     11 Dec, 2016    Init version
"""
from Field import Deck, Pile, Stack


def klondike(deck):
    """Creates board for klondike solitaire"""
    fields = list()
    fields.append(Deck(20, 20))

    fields.append(Pile(20, 112))
    fields.append(Pile(83, 112))
    fields.append(Pile(146, 112))
    fields.append(Pile(209, 112))
    fields.append(Pile(272, 112))
    fields.append(Pile(335, 112))
    fields.append(Pile(398, 112))

    fields.append(Stack(209, 20))
    fields.append(Stack(272, 20))
    fields.append(Stack(335, 20))
    fields.append(Stack(398, 20))

    return klondike_shuffle(fields, deck)


def klondike_shuffle(fields, deck):
    fields[0].add(deck[:24])

    deck[24].show()
    fields[1].add(deck[24])

    fields[2].add(deck[25])
    deck[26].show()
    fields[2].add(deck[26])

    fields[3].add(deck[27:29])
    deck[29].show()
    fields[3].add(deck[29])

    fields[4].add(deck[30:33])
    deck[33].show()
    fields[4].add(deck[33])

    fields[5].add(deck[34:38])
    deck[38].show()
    fields[5].add(deck[38])

    fields[6].add(deck[39:44])
    deck[44].show()
    fields[6].add(deck[44])

    fields[7].add(deck[45:51])
    deck[51].show()
    fields[7].add(deck[51])

    return fields
