from unittest import TestCase
from Application import Application
import pygame
from time import sleep
from Card import Card, Suit
from Board import *
from Field import Field
import xml.dom.minidom


class TestMainApp(TestCase):
    def setUp(self):
        self.app = Application()
        self.app.load_deck()
        self.app.load_fields("klondike")

    def test_load_deck(self):
        # checking length of decks
        self.assertEqual(52, len(self.app._deck))
        self.assertEqual(104, len(self.app._double_deck))

        # checking if there are no two reference to the same object
        self.assertEqual(len(set(self.app._deck)), len(self.app._deck))
        self.assertEqual(len(set(self.app._double_deck)),
                         len(self.app._double_deck))

    def test_load_fields(self):
        # check if good number of fields
        self.assertTrue(12, len(self.app._board))

        # check types of fields
        self.assertTrue(isinstance(self.app._board[0], Deck))
        for field in self.app._board[1:8]:
            self.assertTrue(isinstance(field, Pile))
        for field in self.app._board[8:]:
            self.assertTrue(isinstance(field, Stack))

    def test_remove_from_fields(self):
        card = self.app._board[0].show_cards()[0]
        self.app.remove_from_fields([card])
        for field in self.app._board:
            self.assertFalse(card in field.show_cards())

    def test_check_cards(self):
        # put mouse on place without any card
        pygame.mouse.set_pos(0, 0)
        sleep(2)
        self.assertFalse(self.app.check_cards())
        # put mouse on some card
        pygame.mouse.set_pos(25, 50)
        sleep(2)
        self.assertFalse(self.app.check_cards())

    def test_check_menu(self):
        # put mouse outside the menu
        pygame.mouse.set_pos(100, 100)
        self.assertFalse(self.app.check_menu())
        # put mouse on one of the buttons
        pygame.mouse.set_pos(5, 5)
        self.assertFalse(self.app.check_menu())


class TestCard(TestCase):
    def setUp(self):
        self.app = Application()
        self.king_pik = Card(Suit.pik, self.app._ranks.K, 0, 0)
        self.dame_kier = Card(Suit.kier, self.app._ranks.D, 10, 10)
        self.doc = xml.dom.minidom.Document()
        self.xml_card = self.doc.createElement("Card")
        self.xml_card.setAttribute("rank", self.app._ranks.D.name)
        self.xml_card.setAttribute("suit", Suit.kier.name)

    def test_change_card_position(self):
        self.king_pik.change(50, 75)
        self.assertEqual(50, self.king_pik._x)
        self.assertEqual(75, self.king_pik._y)

    def test_red_black(self):
        self.assertTrue(self.king_pik.red_black(self.dame_kier))
        self.assertFalse(self.king_pik.red_black(self.king_pik))

    def test_next_lower(self):
        self.assertFalse(self.dame_kier.next_lower(self.king_pik))
        self.assertTrue(self.king_pik.next_lower(self.dame_kier))

    def test_is_xml_card(self):
        self.assertFalse(self.king_pik.is_xml_card(self.xml_card))
        self.assertTrue(self.dame_kier.is_xml_card(self.xml_card))


class TestBoard(TestCase):
    def setUp(self):
        self.app = Application()
        self.app.load_deck()

    def test_algerian_create(self):
        fields = algerian(self.app._double_deck)
        # check numbers of fields
        self.assertTrue(17, len(fields))
        # check types of fields
        for field in fields[:8]:
            self.assertTrue(isinstance(field, Stack))
        for field in fields[8:16]:
            self.assertTrue(isinstance(field, Pile))
        self.assertTrue(isinstance(fields[16], LongDeck))

    def test_algerian_shuffle(self):
        fields = algerian(self.app._double_deck)
        fields = algerian_shuffle(fields, self.app._double_deck)
        for field in fields[:8]:
            self.assertFalse(field.show_cards())
        for field in fields[8:12]:
            self.assertTrue(len(field.show_cards()) == 2)
        for field in fields[12:16]:
            self.assertTrue(len(field.show_cards()) == 1)
        self.assertTrue(len(fields[16].show_cards()) == 68)
        for field in fields[16].show_subfields():
            self.assertTrue(len(field.show_cards()) == 4)

    def test_canfield_create(self):
        fields = canfield(self.app._deck)
        # check number of fields
        self.assertEqual(10, len(fields))
        # check types of fields
        for field in fields[:4]:
            self.assertTrue(isinstance(field, Stack))
        self.assertTrue(isinstance(fields[4], Deck))
        for field in fields[5:9]:
            self.assertTrue(isinstance(field, Pile))
        self.assertTrue(isinstance(fields[9], UnputtablePile))

    def test_canfield_shuffle(self):
        fields = canfield(self.app._deck)
        fields = canfield_shuffle(fields, self.app._deck)
        for field in fields[:4]:
            self.assertFalse(field.show_cards())
        self.assertEqual(34, len(fields[4].show_cards()))
        for field in fields[5:9]:
            self.assertEqual(1, len(field.show_cards()))
        self.assertEqual(14, len(fields[9].show_cards()))

    def test_fifteen_puzzle_create(self):
        fields = fifteen_puzzle(self.app._deck)
        # check number of fields
        self.assertEqual(15, len(fields))
        # chcek type of fields
        for field in fields:
            self.assertTrue(isinstance(field, Fours))

    def test_fifteen_puzzle_shuffle(self):
        fields = fifteen_puzzle(self.app._deck)
        fields = fifteen_puzzle_shuffle(fields, self.app._deck)
        for field in fields[:13]:
            self.assertEqual(4, len(field.show_cards()))
        self.assertEqual(0, len(fields[13].show_cards()))
        self.assertEqual(0, len(fields[14].show_cards()))

    def test_klondike_create(self):
        fields = klondike(self.app._deck)
        self.assertEqual(12, len(fields))
        self.assertTrue(isinstance(fields[0], Deck))
        for field in fields[1:8]:
            self.assertTrue(isinstance(field, Pile))
        for field in fields[8:]:
            self.assertTrue(isinstance(field, Stack))

    def test_klondike_shuffle(self):
        fields = klondike(self.app._deck)
        fields = klondike_shuffle(fields, self.app._deck)
        self.assertEqual(24, len(fields[0].show_cards()))
        for i, field in enumerate(fields[1:8]):
            self.assertEqual(i+1, len(field.show_cards()))

    def test_natali_create(self):
        fields = natali(self.app._double_deck)
        self.assertEqual(17, len(fields))
        for field in fields[:8]:
            self.assertTrue(isinstance(field, Stack))
        for field in fields[8:16]:
            self.assertTrue(isinstance(field, Pile))
        self.assertTrue(isinstance(fields[16], Deck))

    def test_natali_shuffle(self):
        fields = natali(self.app._double_deck)
        fields = natali_shuffle(fields, self.app._double_deck)
        for field in fields[:8]:
            self.assertFalse(field.show_cards())
        for i, field in enumerate(fields[8:16:-1]):
            self.assertEqual(i+1, len(field.show_cards()))
        self.assertEqual(68, len(fields[16].show_cards()))

    def test_osmosis_create(self):
        fields = osmosis(self.app._deck)
        self.assertEqual(9, len(fields))
        for field in fields[:4]:
            self.assertTrue(isinstance(field, Fours))
        for field in fields[4:8]:
            self.assertTrue(isinstance(field, Cascade))
        self.assertTrue(isinstance(fields[8], Deck))

    def test_osmosis_shuffle(self):
        fields = osmosis(self.app._deck)
        fields = osmosis_shuffle(fields, self.app._deck)
        for field in fields[:4]:
            self.assertEqual(4, len(field.show_cards()))
        self.assertEqual(1, len(fields[4].show_cards()))
        for field in fields[5:8]:
            self.assertEqual(0, len(field.show_cards()))
        self.assertEqual(35, len(fields[8].show_cards()))


class TestFields(TestCase):
    def setUp(self):
        self.app = Application()
        self.app.load_deck()
        self.field = Pile(0, 0)
        self.dame_kier = Card(Suit.kier, self.app._ranks.D, 20, 20)
        self.as_pik = Card(Suit.pik, self.app._ranks.AS, 20, 20)
        self.as_karo = Card(Suit.karo, self.app._ranks.AS, 20, 20)
        self.walet_trefl = Card(Suit.trefl, self.app._ranks.W, 20, 20)
        self.dame_trefl = Card(Suit.trefl, self.app._ranks.D, 20, 20)

    def test_clicked(self):
        pygame.mouse.set_pos(100, 100)
        self.assertEqual(0, self.field.clicked())
        pygame.mouse.set_pos(3, 3)
        self.assertEqual(0, self.field.clicked())

    def test_add(self):
        self.field.add(self.app._deck[0])
        self.field.add(self.app._deck[1:3])
        self.assertEqual(3, len(self.field.show_cards()))

    def test_take(self):
        self.field.add(self.app._deck[0])
        self.field.take([self.app._deck[0]])
        self.assertEqual(0, len(self.field.show_cards()))

    def test_clear(self):
        self.field.add(self.app._deck)
        self.field.clear()
        self.assertEqual(0, len(self.field.show_cards()))

    def test_deck_index(self):
        deck = Deck(0, 0)
        self.assertEqual(-1, deck.get_index())
        deck.set_index(5)
        self.assertEqual(5, deck.get_index())
        deck.reset()
        self.assertEqual(-1, deck.get_index())

    def test_pile_put(self):
        card, field = self.field.put([self.dame_kier])
        self.assertEqual(self.dame_kier, card[0])
        self.assertEqual(field, self.field)

        self.field.add(self.dame_kier)
        card, field = self.field.put([self.as_pik])
        self.assertEqual(card[0], self.dame_kier)
        self.assertFalse(field)

        card, field = self.field.put([self.as_karo])
        self.assertEqual(card[0], self.dame_kier)
        self.assertFalse(field)

        card, field = self.field.put([self.walet_trefl])
        self.assertEqual(card[0], self.walet_trefl)
        self.assertEqual(field, self.field)

    def test_stack_put(self):
        stack = Stack(20, 20)
        card, field = stack.put([self.as_pik])
        self.assertEqual(card[0], self.as_pik)
        self.assertEqual(field, stack)

        card, field = stack.put([self.walet_trefl])
        self.assertFalse(card)
        self.assertEqual(field, stack)

        stack.add(self.walet_trefl)
        card, field = stack.put([self.dame_trefl])
        self.assertEqual(card[0], self.dame_trefl)
        self.assertEqual(field, stack)

        card, field = stack.put([self.as_karo])
        self.assertEqual(self.walet_trefl, card[0])
        self.assertFalse(field)

    def test_fours_put(self):
        fours = Fours(20, 20)

        card, field = fours.put([self.as_pik])
        self.assertEqual(card[0], self.as_pik)
        self.assertEqual(field, fours)

        card, field = fours.put([self.as_pik, self.walet_trefl])
        self.assertFalse(card)
        self.assertEqual(field, fours)

        fours.add([self.as_pik])
        card, field = fours.put([self.walet_trefl])
        self.assertFalse(card)
        self.assertEqual(field, fours)

        card, field = fours.put([self.as_karo])
        self.assertEqual(card[0], self.as_karo)
        self.assertEqual(field, fours)
