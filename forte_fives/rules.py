import card

""""
This file contains the rules of the game 45s.

The functions provided here should be used as helper functions
throughout the game whenever a game rule needs to be followed.
"""

BIDS = (15, 20, 25, 30)

WINNING_SCORE = 120

# Orders are from lowest to highest.
# 'AH' represents the card Ace of Hearts.
IN_SUIT_ORDER_RED = (
    '2', '3', '4', '6', '7', '8', '9', '10', 'Q', 'K', 'AH', 'A', '5', 'J')
IN_SUIT_ORDER_BLACK = (
    '10', '9', '8', '7', '6', '4', '3', '2', 'Q', 'K', 'AH', 'A', '5', 'J')
OUT_SUIT_ORDER_RED = (
    'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
OUT_SUIT_ORDER_BLACK = (
    '10', '9', '8', '7', '6', '5', '4', '3', '2', 'A', 'J', 'Q', 'K')

# Minimum amount of cards that can not be discarded.
MINIMUM_KEEP = 2

HAND_SIZE = 5


class RulesException(Exception):
    pass


def select_valid_bids(current_bid):
    """
    Returns a list of bids that the player is allowed to place.
    A player must place a bid higher than the current_bid.
    """
    # No bid has taken place, yet.
    if current_bid is None or current_bid == 0:
        return BIDS
    # The maximum bid already has been placed.
    if current_bid == BIDS[-1]:
        return []
    # All higher bids are possible.
    i = BIDS.index(current_bid)
    # Don't worry about index out of range. If current_bid is the
    # last bid, the code won't get here.
    return BIDS[i+1:]


def select_valid_cards(suit, hand, cards_played):
    """
    Based on the given hand, return a list of all the cards
    that are allowed to be played.

    If no cards have been played yet, any card may be played.
    If the first played card is out of suit, any card can be played.
    However, if the first played card is in suit, the player has
    to play a card with matching suit. If the player does not
    have any cards in suit, the player is allowed to play any card.
    """
    # No cards have been played.
    if not cards_played:
        return hand.get_all_cards()

    # First card played is out of suit.
    if cards_played[0].suit != suit:
        return hand.get_all_cards()

    # First card played is in suit.
    in_suit = get_in_suit_cards(suit, hand)
    # If hand has any cards in suit.
    if in_suit:
        return in_suit
    # Hand has no cards in suit.
    else:
        return hand.get_all_cards()


def get_in_suit_cards(suit, cards):
    """
    Returns all the cards in the given suit.
    Ace of Hearts is also included in selection.
    """
    return [c for c in cards
            if c.suit == suit or
            (c.suit == card.HEARTS and c.rank == 'A')]


def get_out_suit_cards(suit, cards):
    """
    Returns all the cards that are NOT in the given suit.
    Ace of Hearts is NEVER included in selection.
    """
    return [c for c in cards
            if c.suit != suit and
            not (c.suit == card.HEARTS and c.rank == 'A')]


def get_card_order_for_suit(suit, in_suit=True):
    """
    Returns the correct card order for the given suit. in_suit is
    used to get the card order for when the turn is played in suit
    or out of suit.
    """
    if in_suit:
        if card.SUIT_COLOR[suit] == card.RED_SUIT:
            return IN_SUIT_ORDER_RED
        else:
            return IN_SUIT_ORDER_BLACK
    else:
        if card.SUIT_COLOR[suit] == card.RED_SUIT:
            return OUT_SUIT_ORDER_RED
        else:
            return OUT_SUIT_ORDER_BLACK


def get_highest_card_in_suit(suit, cards):
    """
    Returns the highest card in suit of the given cards.
    An exception is raised if no cards in suit are present.
    """
    # Filter out the non-suit cards.
    cards = get_in_suit_cards(suit, cards)
    if len(cards) == 0:
        raise RulesException("Need at least one card in suit!")
    if len(cards) == 1:
        return cards[0]

    cards_order = get_card_order_for_suit(suit)

    highest_index = -1
    highest_card = None
    for c in cards:
        rank = c.rank
        # Adjust for Ace of Hearts.
        if c.suit == card.HEARTS and c.rank == 'A':
            rank = 'AH'
        current_index = cards_order.index(rank)
        if current_index > highest_index:
            highest_index = current_index
            highest_card = c

    if highest_card is None:
        raise RulesException('Unexpected error! Unable to find highest card.')

    return highest_card


def get_highest_card_out_suit(cards):
    """
    Returns the highest card out suit of the given cards.
    The first card determines what suit is played in.
    """
    return get_highest_card_in_suit(cards[0].suit, cards)


def get_winnind_card(suit, cards):
    """
    Return the card that "won" this turn.
    """

    if len(cards) == 0:
        raise RulesException("Need at least one card to get winner!")

    # Determine whether or not this turn was played in suit.
    in_suit = len(get_in_suit_cards(suit, cards)) > 0

    if in_suit:
        # When in_suit we can ignore all the out suit cards.
        return get_highest_card_in_suit(suit, cards)

    else:
        return get_highest_card_out_suit(cards)
