from forte_fives import card


class Hand(object):
    """
    This class represents a hand of cards.
    """

    def __init__(self):
        self.cards = []

    def __len__(self):
        """
        Returns the length of hand (how many
        cards in hand.
        """
        return len(self.cards)

    def __str__(self):
        """
        String representation of Hand.
        """
        return ' | '.join([str(card) for card in self.cards])

    def __iter__(self):
        """
        Makes Hand iterable on its cards.
        """
        for card in self.cards:
            yield card

    def add_card(self, card):
        """
        Adds a card to the hand.
        """
        self.cards.append(card)

    def remove_card(self, card):
        """
        Removes a specific card from hand.
        """
        self.cards.remove(card)

    def get_cards_in_suit(self, suit):
        """
        Returns all the cards in hand that match suit.
        """
        if suit not in card.SUITS:
            raise card.BadSuitException('Invalid card suit, %s' % suit)

        return [card for card in self.cards if card.suit == suit]

    def get_all_cards(self):
        """
        Returns all cards in hand.
        """
        return self.cards
