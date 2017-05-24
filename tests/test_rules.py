from forte_fives import card
from forte_fives import hand
from forte_fives import rules

import unittest


class TestRulesModule(unittest.TestCase):

    ###########################################################################
    #
    # rules.select_valid_bids() test cases.
    #
    ###########################################################################

    def testSelectValidBids_NoneBid(self):
        """All bids are selected if current bid is None.
        """
        self.assertTrue(rules.select_valid_bids(None) == rules.BIDS)

    def testSelectValidBids_0Bid(self):
        """All bids are selected if current bid is 0.
        """
        self.assertTrue(rules.select_valid_bids(0) == rules.BIDS)

    def testSelectValidBids_HigherBids(self):
        """Bids higher than current bid are selected.
        """
        self.assertTrue(rules.select_valid_bids(20) == (25, 30))

    def testSelectValidBids_HighestBid(self):
        """Highest bid already placed. No more bids allowed.
        """
        self.assertEqual(rules.select_valid_bids(30), [])

    ###########################################################################
    #
    # rules.select_valid_cards() test cases.
    #
    ###########################################################################

    def testSelectValidCards_NoCardsPlayed(self):
        """All cards are selected if no cards have been played yet.
        """
        cards = [card.Card('2', card.CLUBS),
                 card.Card('3', card.CLUBS),
                 card.Card('4', card.CLUBS),
                 card.Card('5', card.CLUBS),
                 card.Card('6', card.CLUBS)]
        hand1 = hand.Hand()
        for c in cards:
            hand1.add_card(c)

        selected_cards = rules.select_valid_cards(card.CLUBS, hand1, [])
        for c in cards:
            self.assertTrue(c in selected_cards)

    def testSelectValidCards_InSuit(self):
        """In suit cards selected if in suit card played first.
        """
        in_suit_cards = [card.Card('2', card.CLUBS),
                         card.Card('3', card.CLUBS),
                         card.Card('4', card.CLUBS)]
        out_suit_cards = [card.Card('2', card.DIAMONDS),
                          card.Card('4', card.HEARTS)]
        hand1 = hand.Hand()
        # Mix up the cards just in case.
        hand1.add_card(out_suit_cards[0])
        for c in in_suit_cards:
            hand1.add_card(c)
        hand1.add_card(out_suit_cards[1])

        selected_cards = rules.select_valid_cards(card.CLUBS, hand1,
                                                  [card.Card('K', card.CLUBS)])
        for c in in_suit_cards:
            self.assertTrue(c in selected_cards)
        for c in out_suit_cards:
            self.assertFalse(c in selected_cards)

    def testSelectValidCards_InSuitMissing(self):
        """All selected if in suit played first but no in suit cards available.
        """
        cards = [card.Card('2', card.DIAMONDS),
                 card.Card('2', card.CLUBS),
                 card.Card('3', card.CLUBS),
                 card.Card('4', card.CLUBS),
                 card.Card('4', card.HEARTS)]
        hand1 = hand.Hand()

        for c in cards:
            hand1.add_card(c)

        selected_cards = rules.select_valid_cards(
            card.CLUBS, hand1, [card.Card('K', card.SPADES)])
        for c in cards:
            self.assertTrue(c in selected_cards)

    def testSelectValidCards_OutSuit(self):
        """All cards selected if out suit card played first.
        """
        cards = [card.Card('2', card.DIAMONDS),
                 card.Card('2', card.CLUBS),
                 card.Card('3', card.SPADES),
                 card.Card('4', card.CLUBS),
                 card.Card('4', card.HEARTS)]
        hand1 = hand.Hand()

        for c in cards:
            hand1.add_card(c)

        selected_cards = rules.select_valid_cards(
            card.CLUBS, hand1, [card.Card('K', card.HEARTS)])
        for c in cards:
            self.assertTrue(c in selected_cards)

    ###########################################################################
    #
    # rules.get_in_suit_cards() test cases.
    #
    ###########################################################################

    def testGetInSuitCards_InSuit(self):
        """All cards in suit are returned.
        """
        in_suit_cards = [card.Card('2', card.CLUBS),
                         card.Card('3', card.CLUBS),
                         card.Card('4', card.CLUBS)]
        out_suit_cards = [card.Card('2', card.DIAMONDS),
                          card.Card('4', card.HEARTS)]
        cards = in_suit_cards + out_suit_cards
        returned_cards = rules.get_in_suit_cards(card.CLUBS, cards)

        for c in in_suit_cards:
            self.assertTrue(c in returned_cards)
        for c in out_suit_cards:
            self.assertFalse(c in returned_cards)

    def testGetInSuitCards_NoSuit(self):
        """No cards are returned if no suit cards available.
        """
        cards = [card.Card('2', card.DIAMONDS),
                 card.Card('2', card.CLUBS),
                 card.Card('3', card.CLUBS),
                 card.Card('4', card.CLUBS),
                 card.Card('4', card.HEARTS)]

        returned_cards = rules.get_in_suit_cards(card.SPADES, cards)
        self.assertTrue(len(returned_cards) == 0)

    def testGetInSuitCards_AceOfHearts(self):
        """Ace of Hearts is returned when suit is not Hearts.
        """
        in_suit_cards = [card.Card('2', card.CLUBS),
                         card.Card('3', card.CLUBS),
                         card.Card('A', card.HEARTS)]
        out_suit_cards = [card.Card('2', card.DIAMONDS),
                          card.Card('4', card.HEARTS)]
        cards = in_suit_cards + out_suit_cards
        returned_cards = rules.get_in_suit_cards(card.CLUBS, cards)

        for c in in_suit_cards:
            self.assertTrue(c in returned_cards)
        for c in out_suit_cards:
            self.assertFalse(c in returned_cards)

    ###########################################################################
    #
    # rules.get_out_suit_cards() test cases.
    #
    ###########################################################################

    def testGetOutSuitCards_InSuit(self):
        """All cards in suit are excluded.
        """
        in_suit_cards = [card.Card('2', card.CLUBS),
                         card.Card('3', card.CLUBS),
                         card.Card('4', card.CLUBS)]
        out_suit_cards = [card.Card('2', card.DIAMONDS),
                          card.Card('4', card.HEARTS)]
        cards = in_suit_cards + out_suit_cards
        returned_cards = rules.get_out_suit_cards(card.CLUBS, cards)
        for c in in_suit_cards:
            self.assertFalse(c in returned_cards)
        for c in out_suit_cards:
            self.assertTrue(c in returned_cards)

    def testGetOutSuitCards_NoSuit(self):
        """No cards are returned if no out suit cards available.
        """
        cards = [card.Card('2', card.SPADES),
                 card.Card('3', card.SPADES),
                 card.Card('4', card.SPADES),
                 card.Card('5', card.SPADES),
                 card.Card('J', card.SPADES)]

        returned_cards = rules.get_out_suit_cards(card.SPADES, cards)
        self.assertTrue(len(returned_cards) == 0)

    def testGetOutSuitCards_AceOfHearts(self):
        """Ace of Hearts is not returned when suit is not Hearts.
        """
        in_suit_cards = [card.Card('2', card.CLUBS),
                         card.Card('3', card.CLUBS),
                         card.Card('A', card.HEARTS)]
        out_suit_cards = [card.Card('2', card.DIAMONDS),
                          card.Card('4', card.HEARTS)]
        cards = in_suit_cards + out_suit_cards
        returned_cards = rules.get_out_suit_cards(card.CLUBS, cards)

        for c in in_suit_cards:
            self.assertFalse(c in returned_cards)
        for c in out_suit_cards:
            self.assertTrue(c in returned_cards)

    ###########################################################################
    #
    # rules.get_card_order_for_suit() test cases.
    #
    ###########################################################################

    def testGetCardOrderForSuit_DiamondsInSuit(self):
        """In suit red card order is returned.
        """
        self.assertEqual(rules.get_card_order_for_suit(card.DIAMONDS),
                         rules.IN_SUIT_ORDER_RED)

    def testGetCardOrderForSuit_HeartsInSuit(self):
        """In suit red card order is returned.
        """
        self.assertEqual(rules.get_card_order_for_suit(card.HEARTS),
                         rules.IN_SUIT_ORDER_RED)

    def testGetCardOrderForSuit_ClubsInSuit(self):
        """In suit black card order is returned.
        """
        self.assertEqual(rules.get_card_order_for_suit(card.CLUBS),
                         rules.IN_SUIT_ORDER_BLACK)

    def testGetCardOrderForSuit_SpadesInSuit(self):
        """In suit black card order is returned.
        """
        self.assertEqual(rules.get_card_order_for_suit(card.SPADES),
                         rules.IN_SUIT_ORDER_BLACK)

    def testGetCardOrderForSuit_DiamondsOutSuit(self):
        """Out suit red card order is returned.
        """
        self.assertEqual(rules.get_card_order_for_suit(card.DIAMONDS, False),
                         rules.OUT_SUIT_ORDER_RED)

    def testGetCardOrderForSuit_HeartsOutSuit(self):
        """Out suit red card order is returned.
        """
        self.assertEqual(rules.get_card_order_for_suit(card.HEARTS, False),
                         rules.OUT_SUIT_ORDER_RED)

    def testGetCardOrderForSuit_ClubsOutSuit(self):
        """Out suit black card order is returned.
        """
        self.assertEqual(rules.get_card_order_for_suit(card.CLUBS, False),
                         rules.OUT_SUIT_ORDER_BLACK)

    def testGetCardOrderForSuit_SpadesOutSuit(self):
        """Out suit black card order is returned.
        """
        self.assertEqual(rules.get_card_order_for_suit(card.SPADES, False),
                         rules.OUT_SUIT_ORDER_BLACK)

    ###########################################################################
    #
    # rules.get_highest_card_in_suit() test cases.
    #
    ###########################################################################

    def testGetHighestCardInSuit_Invalid(self):
        """Exception is raised if no cards available in suit.
        """
        cards = [card.Card('2', card.DIAMONDS),
                 card.Card('2', card.SPADES),
                 card.Card('3', card.SPADES),
                 card.Card('4', card.SPADES),
                 card.Card('4', card.HEARTS)]

        self.assertRaises(rules.RulesException,
                          rules.get_highest_card_in_suit,
                          card.CLUBS, cards)

    def testGetHighestCardInSuit_AceOfHearts(self):
        """Ace of Hearts is detected as highest card.
        """
        highest = card.Card('A', card.HEARTS)
        cards = [card.Card('9', card.SPADES),
                 card.Card('2', card.SPADES),
                 card.Card('3', card.SPADES),
                 highest,
                 card.Card('K', card.SPADES)]

        self.assertEqual(rules.get_highest_card_in_suit(card.SPADES, cards),
                         highest)

    def testGetHighestCardInSuit_HighestCard(self):
        """Highest card is detected.
        """
        highest = card.Card('5', card.SPADES)
        cards = [card.Card('9', card.SPADES),
                 card.Card('2', card.SPADES),
                 card.Card('3', card.SPADES),
                 highest,
                 card.Card('K', card.SPADES)]

        self.assertEqual(rules.get_highest_card_in_suit(card.SPADES, cards),
                         highest)

    ###########################################################################
    #
    # rules.get_highest_card_out_suit() test cases.
    #
    ###########################################################################

    def testGetHighestCardOutSuit(self):
        """Highest card out of suit is detected.
        """
        highest = card.Card('5', card.HEARTS)
        cards = [highest,
                 card.Card('2', card.HEARTS),
                 card.Card('Q', card.CLUBS),
                 card.Card('5', card.DIAMONDS),
                 card.Card('K', card.CLUBS)]

        self.assertEqual(rules.get_highest_card_out_suit(cards), highest)

    ###########################################################################
    #
    # rules.get_winnind_card() test cases.
    #
    ###########################################################################

    def testGetWinningCard_Invalid(self):
        """Exception is raised if cards is empty.
        """
        self.assertRaises(rules.RulesException, rules.get_winnind_card,
                          card.CLUBS, [])

    def testGetWinningCard_InSuite(self):
        """Correct highest in suit card is detected.
        """
        highest = card.Card('5', card.SPADES)
        cards = [card.Card('9', card.SPADES),
                 card.Card('2', card.SPADES),
                 card.Card('3', card.SPADES),
                 highest,
                 card.Card('K', card.SPADES)]

        self.assertEqual(rules.get_winnind_card(card.SPADES, cards), highest)

    def testGetWinningCard_InSuiteMiddle(self):
        """Highest in suit card is detected when first card is out of suit.
        """
        highest = card.Card('5', card.SPADES)
        cards = [card.Card('9', card.HEARTS),
                 card.Card('2', card.SPADES),
                 card.Card('3', card.SPADES),
                 highest,
                 card.Card('K', card.SPADES)]

        self.assertEqual(rules.get_winnind_card(card.SPADES, cards), highest)

    def testGetWinningCard_OutSuite(self):
        """Correct highest out suit card is detected."""
        highest = card.Card('5', card.HEARTS)
        cards = [highest,
                 card.Card('2', card.HEARTS),
                 card.Card('Q', card.CLUBS),
                 card.Card('5', card.DIAMONDS),
                 card.Card('K', card.CLUBS)]

        self.assertTrue(rules.get_winnind_card(card.SPADES, cards) == highest)

if __name__ == "__main__":
    unittest.main()
