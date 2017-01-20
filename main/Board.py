"""
Created by pikuldorota

History of modification:
pikuldorota     11 Dec, 2016    Init version
pikuldorota     16 Dec, 2016    Change klondike to fit with menu
pikuldorota     17 Dec, 2016    Add fifteen puzzle
pikuldorota     28 Dec, 2016    Add canfield and slightly change positions of some fields
pikuldorota      7 Jan, 2017    Add functions for checking if game was solved
pikuldorota     20 Jan, 2017    Add skeletons for algiernian and osmosis patience
"""
from Field import Deck, Pile, Stack, Fours
from random import shuffle


def klondike(deck):
    """Creates board for klondike solitaire"""
    fields = [Deck(20, 45), Pile(20, 145), Pile(94, 145), Pile(168, 145), Pile(242, 145), Pile(316, 145),
              Pile(390, 145), Pile(463, 145), Stack(242, 45), Stack(316, 45), Stack(390, 45), Stack(463, 45)]

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


def klondike_is_finished(fields):
    """Checks if klondike has been solved"""
    if len(fields[8].show_cards()) == len(fields[9].show_cards()) ==\
            len(fields[10].show_cards()) == len(fields[11].show_cards()) == 13:
        return True
    return False


def fifteen_puzzle(deck):
    """Creates board for fifteen puzzle game"""
    fields = [Fours(92, 45), Fours(277, 45), Fours(463, 45),
              Fours(92, 152), Fours(277, 152), Fours(463, 152),
              Fours(92, 260), Fours(277, 260), Fours(463, 260),
              Fours(92, 370), Fours(277, 370), Fours(463, 370),
              Fours(92, 475), Fours(277, 475), Fours(463, 475)]

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


def fifteen_puzzle_is_finished(fields):
    """Checks if fifteen puzzle has been solved"""
    for field in fields:
        cards = field.show_cards()
        if cards:
            for card in cards[1:]:
                if card.rank().name != cards[0].rank().name:
                    return False
    return True


def canfield(deck):
    """Creates board for canfield game"""
    fields = [Stack(10, 40), Stack(100, 40), Stack(190, 40), Stack(280, 40), Deck(370, 40), Pile(10, 100),
              Pile(100, 100), Pile(190, 100), Pile(270, 100)]
    return canfield_shuffle(fields, deck)


def canfield_shuffle(fields, deck):
    """Puts card on canfield board"""
    clean_and_shuffle(fields, deck)
    fields[4].add(deck[:48])
    fields[5].add(deck[48])
    fields[6].add(deck[49])
    fields[7].add(deck[50])
    fields[8].add(deck[51])
    return fields


def canfield_is_finished(fields):
    """Checks if canfield has been solved"""
    return False


def clock(deck, ranks):
    """Creates board for clock patience"""
    fields = []
    X = [92, 102, 112, 192, 132, 152, 392, 142, 132, 122, 112, 102, 132]
    Y = [35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35]
    for x, y, rank in zip(X,Y,ranks):
        fields.append(Fours(x, y, rank))
    return clock_shuffle(fields, deck)


def clock_shuffle(fields, deck):
    """Shuffles cards and put them on clock board"""
    clean_and_shuffle(fields, deck)

    for card in deck:
        card.hide()

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


def clock_is_finished(fields):
    """Checks if clock game has been finished"""
    return False


def algiernian(deck):
    pass


def algiernian_shuffle(fields, deck):
    pass


def algiernian_is_finished(fields):
    pass


def osmosis(deck):
    pass


def osmosis_shuffle(fields, deck):
    pass


def osmosis_is_finished(fields):
    pass


def clean_and_shuffle(fields, deck):
    """Shuffles deck and removes cards from fields"""
    shuffle(deck)
    for field in fields:
        field.clear()
