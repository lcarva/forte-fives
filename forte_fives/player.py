import card
import intel
import rules


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


class HumanPlayer(Player):
    """
    This class defines a player that performs actions based
    on user input.
    """

    def place_bid(self, current_bid):
        """
        Prompt the user to determine whether or not
        to place a bid.
        """
        # Change None value of bid to 0 for easy usage.
        if current_bid is None:
            current_bid = 0
        print 'Your hand is', self.hand
        print 'Current bid is %d.' % current_bid
        prompt_msg = ('How much is your bid? ' +
                      '(Either 0 or higher than current bid) ')
        bid = -1
        while bid not in rules.select_valid_bids(current_bid) and bid != 0:
            bid = int(raw_input(prompt_msg))

        return bid

    def select_suit(self):
        """
        Prompt the user to select which suit to play.
        """
        print 'Your hand is', self.hand
        print 'Select what suit to play:'
        suit = ''
        while suit not in card.SUITS:
            suit = raw_input('[clubs, diamonds, hearts, spades]: ')
        return suit

    def _select_card(self, suit, cards_played):
        """
        Prompt the user for what card to play.
        """
        valid_cards = rules.select_valid_cards(suit, self.hand, cards_played)
        print 'Cards played in order', cards_played
        print 'Your hand is', self.hand
        while True:
            card_index = int(raw_input('Enter 0-based card number: '))
            if card_index >= len(self.hand.cards):
                print 'Bad selection! Try again.'
            else:
                selected_card = self.hand.cards[card_index]
                if selected_card in valid_cards:
                    return selected_card

    def _select_discard_cards(self, suit):
        """
        Prompt the user for what cards to discard.
        """
        print 'Your hand is', self.hand
        selected_cards = []
        selected_indexes = []
        # Determine maximum amount of cards that can be discarded.
        max_amount = len(self.hand) - rules.MINIMUM_KEEP

        while len(selected_cards) < max_amount:
            card_index = int(raw_input('Enter 0-based card [-1 to end]: '))
            if card_index == -1:
                if len(self.hand) - len(selected_cards) > rules.HAND_SIZE:
                    print 'Not enough cards discarded.'
                    continue
                else:
                    break
            if (card_index >= len(self.hand.cards) or
                    card_index in selected_indexes):
                print 'Bad selection! Try again.'
            else:
                selected_indexes.append(card_index)
                selected_cards.append(self.hand.cards[card_index])

        return selected_cards
