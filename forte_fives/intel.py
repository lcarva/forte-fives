import rules

import random


class Intel(object):
    """
    Module that allow a Player to make decisions,
    such as which suit to select, whether or not to bid,
    what card to play and more.
    """

    def __init__(self, player):
        """
        Initializer of Intel.
        """
        self.player = player

    def select_suit(self):
        """
        Returns the suit the player should select as
        the current "playing" suit.
        """

        # Are there any fives?
        fives = [card for card in self.player.hand if card.rank == '5']
        if fives:
            return fives[0].suit

        return random.choice(self.player.hand.cards).suit

    def should_bid(self, current_bid):
        """
        Determines whether or not the player wants to bid
        based on the current bid and Player's hand.
        """

        # TODO: Need to add some AI here.

        possible_bids = rules.select_valid_bids(current_bid)

        if random.choice([True, False, False]):
            return possible_bids[0]
        else:
            return 0

    def select_best_card(self, suit, cards_played):
        """
        Returns the best card to be played based on the suit
        being played and the cards that were already played.
        """
        # For now let's make it really dumb.

        # Just pick a random valid card.
        return random.choice(
                        rules.select_valid_cards(suit, self.player.hand,
                                               cards_played))

    def select_discard_cards(self, suit):
        """
        Returns all the cards that are out of suit up to allowed
        maximum amount.
        """

        # Determine what's the maximum amount of cards that can
        # be discarded. Then, head-slice list to max amount.
        max_amount = len(self.player.hand) - rules.MINIMUM_KEEP
        return rules.get_out_suit_cards(suit, self.player.hand)[:max_amount]
