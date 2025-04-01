import unittest
from start import Card, Deck

class TestCard(unittest.TestCase):
    def setUp(self):
        self.card = Card("h",5)

    def test_card_display(self):
        self.assertEqual(self.card.display(), ("h",5))

class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()

    def test_deck_includes_52_cards(self):
        self.assertEqual(len(self.deck.deck), 52)

    def test_suffle(self):
        ogdeck = self.deck.deck[:]
        self.deck.suffle()
        self.assertNotEqual(self.deck.deck, ogdeck)
