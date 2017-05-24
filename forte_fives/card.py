HEARTS = 'hearts'
DIAMONDS = 'diamonds'
CLUBS = 'clubs'
SPADES = 'spades'

SUITS = (HEARTS, DIAMONDS, CLUBS, SPADES)

RED_SUIT = 'red'
BLACK_SUIT = 'black'

SUIT_COLOR = {
              HEARTS:   RED_SUIT,
              DIAMONDS: RED_SUIT,
              CLUBS:    BLACK_SUIT,
              SPADES:   BLACK_SUIT}

RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')


class ForteFivesException(Exception):
    pass


class BadCardException(ForteFivesException):
    pass


class BadSuitException(ForteFivesException):
    pass


class BadRankException(ForteFivesException):
    pass


class Card(object):

    def __init__(self, rank, suit):
        """
        Initialize rank and suite of the card
        """
        self.rank = rank
        self.suit = suit

        # Perform a simple validation.
        self.validate_card()

        # Assign card color.
        self.color = SUIT_COLOR[self.suit]

    def __str__(self):
        """
        Defines how the card should be printed
        """
        return "%s%s" % (self.rank, self.suit_to_ascii())

    def __repr__(self):
        """
        Object representation of a card.
        """
        return self.__str__()

    def suit_to_ascii(self):
        """
        Short function to convert the suit into ascii
        """
        '''
        if sys.platform == 'win32':
            if self.suit == 'hearts':
                return chr(3)
            elif self.suit == 'diamonds':
                return chr(4)
            elif self.suit == 'clubs':
                return chr(5)
            elif self.suit == 'spades':
                return chr(6)
            else:
                return chr(1)
        # ASCII suits are not supported on Linux or ?Mac
        else:
            return ' of %s' % self.suit.title()
        '''
        return ' of %s' % self.suit.title()

    def validate_card(self):
        """
        Verifies that card was initialized with valid arguments.
        """
        if self.rank not in RANKS:
            raise BadRankException("Invalid rank: %s" % self.rank)
        if self.suit not in SUITS:
            raise BadSuitException("Invalid suit: %s" % self.suit)
