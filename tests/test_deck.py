from forte_fives import card
from forte_fives import deck


import unittest


class Deck_init(unittest.TestCase):

    def setUp(self):
        self.mydeck = deck.Deck()

    def tearDown(self):
        self.mydeck = None

    def test_correct_size(self):
        self.assertTrue(len(self.mydeck.cards) == 52)

    def test_unique_cards(self):
        # Can't use set/frozenset because cards are not hashable.
        # Well... they are but two cards of the same rank and
        # suit will have different hashable values.
        d = dict.fromkeys([str(c) for c in self.mydeck.cards])
        self.assertTrue(len(d) == 52)

    def test_correct_suites(self):
        suits = dict()
        for c in self.mydeck.cards:
            if c.suit not in suits.keys():
                suits[c.suit] = 0
            suits[c.suit] += 1
        for suit in card.SUITS:
            self.assertTrue(suits[suit] == 13)

    def test_correct_ranks(self):
        ranks = dict()
        for c in self.mydeck.cards:
            if c.rank not in ranks.keys():
                ranks[c.rank] = 0
            ranks[c.rank] += 1
        for rank in card.RANKS:
            self.assertTrue(ranks[rank] == 4)


class Deck_len(unittest.TestCase):

    def setUp(self):
        self.mydeck = deck.Deck()

    def tearDown(self):
        self.mydeck = None

    def test_full_deck(self):
        self.assertTrue(len(self.mydeck) == len(self.mydeck.cards) == 52)

    def test_size51(self):
        self.mydeck.cards.pop()
        self.assertTrue(len(self.mydeck) == len(self.mydeck.cards) == 51)

    def test_linked_to_cards_list(self):
        self.mydeck.cards = []
        self.assertTrue(len(self.mydeck) == len(self.mydeck.cards) == 0)


class Deck_contains(unittest.TestCase):

    def setUp(self):
        self.mydeck = deck.Deck()

    def tearDown(self):
        self.mydeck = None

    def test_positive(self):
        self.assertTrue(self.mydeck.cards[10] in self.mydeck)

    def test_negative(self):
        removed_card = self.mydeck.cards.pop()
        self.assertFalse(removed_card in self.mydeck)

    def test_invalid_card_type(self):
        # Any kind of object.
        any_obj = dict()
        self.assertRaises(card.BadCardException, self.mydeck.__contains__,
                          any_obj)


class InsertCard(unittest.TestCase):

    def setUp(self):
        self.mydeck = deck.Deck()

    def tearDown(self):
        self.mydeck = None

    def test_invalid_card_type(self):
        any_obj = dict()
        self.assertRaises(card.BadCardException, self.mydeck.insert_card,
                          any_obj)

    def test_duplicate_card(self):
        self.assertRaises(card.BadCardException, self.mydeck.insert_card,
                          self.mydeck.cards[0])

    def test_valid_insert(self):
        removed_card = self.mydeck.cards.pop()
        self.assertTrue(removed_card not in self.mydeck)
        self.mydeck.insert_card(removed_card)
        self.assertTrue(removed_card in self.mydeck)


class PickCard(unittest.TestCase):

    def setUp(self):
        self.mydeck = deck.Deck()

    def tearDown(self):
        self.mydeck = None

    def test_last_card(self):
        last_card = self.mydeck.cards[-1]
        picked_card = self.mydeck.pick_card()
        self.assertTrue(last_card == picked_card)

    def test_empty_deck(self):
        self.mydeck.cards = []
        picked_card = self.mydeck.pick_card()
        self.assertTrue(picked_card is None)


class Shuffle(unittest.TestCase):

    def test_different_order(self):
        d = deck.Deck()
        unshuffled_cards = list(d.cards)
        self.assertTrue(unshuffled_cards == d.cards)
        d.shuffle()
        self.assertFalse(unshuffled_cards == d.cards)


if __name__ == '__main__':
    unittest.main()
