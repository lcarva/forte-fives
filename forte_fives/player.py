from forte_fives import card
from forte_fives import intel
from forte_fives import rules


class BadMoveException(Exception):
    pass


class Player(object):
    """
    This class performs actions required to play a game.
    """

    def __init__(self, name):
        """
        Initialization of Player object. Creates hand attribute.
        """
        self.name = name
        self.hand = None
        # Create intelligence object.
        self.intel = intel.Intel(self)

    def __str__(self):
        """
        String representation of Player.
        """
        return self.name
        parts = []
        parts.append(self.name)
        for card in self.hand:
            parts.append(str(card))
        return ' | '.join(parts)

    def set_hand(self, hand):
        """
        Sets parameter hand to Player's hand attribute.
        """
        self.hand = hand

    def place_bid(self, current_bid):
        """
        Use intel to determines whether or not the player
        wants to bid.
        """
        return self.intel.should_bid(current_bid)

    def select_suit(self):
        """
        The Player had placed a successful bid, let's choose what
        suit will be played.
        """
        return self.intel.select_suit()

    def play_card(self, suit, cards_played):

        selected_card = self._select_card(suit, cards_played)
        self.hand.remove_card(selected_card)
        return selected_card

    def _select_card(self, suit, cards_played):
        """
        Selects a card from the current hand, based on the
        current suit and the cards that have already been
        played.
        """
        selected_card = self.intel.select_best_card(suit, cards_played)
        return selected_card

    def _select_discard_cards(self, suit):
        """
        Selects the to be discarded cards.
        """
        selected_cards = self.intel.select_discard_cards(suit)
        return selected_cards

    def discard_cards(self, suit):
        """
        Player is allowed to discard up to 3 cards so it can receive
        the same amount of cards back.
        """
        discard_cards = self._select_discard_cards(suit)
        amount_kept = len(self.hand) - len(discard_cards)
        if amount_kept < rules.MINIMUM_KEEP:
            raise BadMoveException('Too few cards kept, %d' % amount_kept)
        if amount_kept > rules.HAND_SIZE:
            raise BadMoveException('Too many cards keps, %d' % amount_kept)
        # Remove each card from hand.
        for c in discard_cards:
            self.hand.remove_card(c)

        # Returns the amount of cards discarded.
        return len(discard_cards)
