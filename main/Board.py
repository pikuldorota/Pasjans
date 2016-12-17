"""
Created by pikuldorota

History of modification:
pikuldorota     11 Dec, 2016    Init version
pikuldorota     16 Dec, 2016    Change klondike to fit with menu
pikuldorota     17 Dec, 2016    Add fifteen puzzle
"""
from Field import Deck, Pile, Stack, Fours
from random import shuffle


def klondike(deck):
    """Creates board for klondike solitaire"""
    fields = [Deck(20, 45), Pile(20, 149), Pile(83, 149), Pile(146, 149), Pile(209, 149), Pile(272, 149),
              Pile(335, 149), Pile(398, 149), Stack(209, 45), Stack(272, 45), Stack(335, 45), Stack(398, 45)]

    return klondike_shuffle(fields, deck)


def klondike_shuffle(fields, deck):
    """Shuffles cards and puts them on board"""
    clean_and_shuffle(fields, deck)
    fields[0].reset()
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


def fifteen_puzzle(deck):
    """Creates board for fifteen puzzle game"""
    fields = [Fours(25, 35), Fours(175, 35), Fours(325, 35), Fours(25, 130), Fours(175, 130), Fours(325, 130),
              Fours(25, 225), Fours(175, 225), Fours(325, 225), Fours(25, 320), Fours(175, 320), Fours(325, 320),
              Fours(25, 415), Fours(175, 415), Fours(325, 415)]

    return fifteen_puzzle_shuffle(fields, deck)


def fifteen_puzzle_shuffle(fields, deck):
    """Shuffle and puts cards on fifteen puzzle board"""
    clean_and_shuffle(fields, deck)

    for card in deck:
        card.show()

    fields[0].add(deck[:4])
    fields[1].add(deck[4:8])
    fields[2].add(deck[8:12])
    fields[3].add(deck[12:16])
    fields[4].add(deck[16:20])
    fields[5].add(deck[20:24])
    fields[6].add(deck[24:28])
    fields[7].add(deck[28:32])
    fields[8].add(deck[32:36])
    fields[9].add(deck[36:40])
    fields[10].add(deck[40:44])
    fields[11].add(deck[44:48])
    fields[12].add(deck[48:52])

    return fields


def clean_and_shuffle(fields, deck):
    shuffle(deck)
    for field in fields:
        field.clear()
