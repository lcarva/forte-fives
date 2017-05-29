from forte_fives import card


import random


class Deck(object):

    def __init__(self):
        """
        Initialize deck class
        """
        # Create 52 cards
        self.cards = []
        for suit in card.SUITS:
            for rank in card.RANKS:
                self.cards.append(card.Card(rank, suit))

    def __str__(self):
        """
        Defines how the deck should be printed
        """
        string = ""
        for card in self.cards:
            string += str(card) + "\t"
        return string

    def __len__(self):
        """
        Returns how many cards in the deck
        """
        return len(self.cards)

    def __contains__(self, unknown_card):
        """
        Returns whether or not the given unknown_card is already
        in the deck.
        """
        if type(unknown_card) != card.Card:
            raise card.BadCardException('Card of type %s' % str(type(card)))
        for c in self.cards:
            if str(c) == str(unknown_card):
                return True
        return False

    ###########################################################################
    #
    # Action Methods
    #
    ###########################################################################
    def pick_card(self):
        """
        Removes and returns the last card of the deck.
        """
        if len(self) > 0:
            return self.cards.pop()
        return None

    def insert_card(self, new_card):
        """
        Inserts a card at the end of the deck.
        """
        if type(new_card) != card.Card:
            raise card.BadCardException('Card of type %s' % type(new_card))
        if new_card in self:
            raise card.BadCardException('Card already in deck %s'
                                        % str(new_card))
        self.cards.append(new_card)

    def shuffle(self):
        """
        Shuffles the whole deck
        """
        random.shuffle(self.cards)
