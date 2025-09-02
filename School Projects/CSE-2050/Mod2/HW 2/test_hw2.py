import unittest
import random
from hw2 import Card, Deck, is_group

class TestCard(unittest.TestCase):
    def test_init(self):
        #Tests that we can initialize cards with number/color/shading/shaper
        card1 = Card(3, "purple", "striped", "diamond")

        self.assertEqual(card1.number, 3)
        self.assertEqual(card1.color, "purple")
        self.assertEqual(card1.shading, "striped")
        self.assertEqual(card1.shape, "diamond")

    def test_str(self):
        #test that we get correct string representation of GroupCard instances
        card1 = Card(1, "purple", "striped", "oval")
        self.assertEqual(card1, "Card(1, purple, striped, oval)")

    def test_eq(self):
        #Tests that two cards are equal if all attributes are equal
        card1 = Card(1, "blue", "empty", "oval")
        card2 = Card(1, "blue", "empty", "oval")
        self.assertEqual(card1, card2)

class TestDeck(unittest.TestCase):
    def test_init(self):
        #Tests that we can initialize a deck of cards
        deck1 = Deck()

    def test_draw_top(self): 
        #Tests that top returns the correct card
        deck1 = Deck()
        self.assertEqual(deck1.draw_top(), "Card(3, purple, solid, oval)")

    def test_shuffle(self):
        #Tests that we can shuffle a deck by checking for a difference in the top card
        random.seed(652)
        deck1 = Deck()
        deck1.shuffle()
        self.assertFalse(deck1.draw_top() == "Card(3, purple, solid, oval)")

class TestSimulator(unittest.TestCase):
    def test_is_group(self): 
        #Tests that it correctly determines if there is a set of cards (attributes are all the same or all different)
        card1 = Card(3, "purple", "solid", "oval")
        card2 = Card(2, "purple", "solid", "diamond")
        card3 = Card(1, "blue", "striped", "oval")
        card4 = Card(3, "green", "empty", "squiggle")

        self.assertFalse(is_group(card1, card2, card3))
        self.assertTrue(is_group(card2, card3, card4))


unittest.main() # runs all unittests above