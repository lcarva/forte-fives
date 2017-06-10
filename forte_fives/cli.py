from forte_fives.player import Player
from forte_fives.game import Game
from forte_fives import card
from forte_fives import rules


from argparse import ArgumentParser
from textwrap import dedent


class CliPlayer(Player):
    """Define player that performs actions based on user input."""

    def place_bid(self, current_bid):
        """Prompt user to determine whether or not to place a bid."""
        # Change None value of bid to 0 for easy usage.
        current_bid = current_bid or 0
        self._display_hand(with_choice=False)
        print('Current bid is {}'.format(current_bid))

        while True:
            valid_bids = rules.select_valid_bids(current_bid)
            message = dedent("""\
                Possible bids are: {}
                What is your bid? (Press ENTER skip): """
                .format(valid_bids))

            raw_bid = raw_input(message).strip()
            try:
                bid = int(raw_bid or 0)
            except ValueError:
                print('{} is not a valid bid!'.format(raw_bid))
                continue

            if bid and bid not in valid_bids:
                print('{} is not a valid bid!'.format(raw_bid))
                continue

            return bid

    def select_suit(self):
        """Prompt user to select which suit to play."""
        self._display_hand(with_choice=False)

        while True:
            self._display_suits(with_choice=False)
            suit = raw_input('Choose suit: ').strip()
            if not suit:
                print('A suit must be selected!')
                continue

            if suit not in card.SUITS:
                print('{} is not a valid suit!'.format(suit))
                continue
            return suit

    def _select_card(self, suit, cards_played):
        """
        Prompt the user for what card to play.
        """
        valid_cards = rules.select_valid_cards(suit, self.hand, cards_played)
        self._display_cards_played(cards_played)
        self._display_hand(with_choice=True)

        while True:
            raw_card_index = raw_input('Enter card selection: ').strip()
            if not raw_card_index:
                print('A card must be chosen!')
                continue

            try:
                card_index = int(raw_card_index)
            except ValueError:
                print('{} is not a valid card selection!'.format(raw_card_index))
                continue

            if card_index >= len(self.hand.cards):
                print('{} is not a valid selection!'.format(card_index))
                continue

            selected_card = self.hand.cards[card_index]
            if selected_card not in valid_cards:
                print('{} is not a valid card!'.format(selected_card))
                continue

            return selected_card

    def _select_discard_cards(self, suit):
        """
        Prompt the user for what cards to discard.
        """
        self._display_hand(with_choice=True)

        selected_cards = []
        selected_indexes = []
        # Determine maximum amount of cards that can be discarded.
        max_amount = len(self.hand) - rules.MINIMUM_KEEP

        while len(selected_cards) < max_amount:
            # TODO: Indicate how many cards must be discarded.
            raw_card_index = raw_input('Enter card selection [Press ENTER to end]: ').strip()
            try:
                card_index = int(raw_card_index or -1)
            except ValueError:
                print('{} is not a valid card selection!'.format(raw_card_index))
                continue

            if card_index == -1:
                if len(self.hand) - len(selected_cards) > rules.HAND_SIZE:
                    print 'Not enough cards discarded.'
                    continue

                break

            if card_index >= len(self.hand.cards):
                print('{} is not a valid card selection!'.format(card_index))
                continue

            if card_index in selected_indexes:
                print('{} card already selected!'.format(card_index))
                continue

            selected_indexes.append(card_index)
            selected_cards.append(self.hand.cards[card_index])

        return selected_cards

    def _display_hand(self, with_choice=True):
        print('Your hand is:')
        self._display_iterable(self.hand.cards, with_choice=with_choice)

    def _display_suits(self, with_choice=True):
        print('Available suits:')
        self._display_iterable(card.SUITS, with_choice=with_choice)

    def _display_cards_played(self, cards_played):
        print('Cards played, in order: ')
        self._display_iterable(cards_played, with_choice=False)

    def _display_iterable(self, iterable, with_choice=True):
        for index, item in enumerate(iterable):
            if with_choice:
                print('[{}] {}'.format(index, item))
            else:
                print(item)


def parse_args():

    parser = ArgumentParser(
            description='Forte-Fives: the not-so-known 45s card game')

    # TODO: Set a max
    parser.add_argument('-p', '--players', type=int, default=3,
            help='Number of computer players (default: 3)')

    return parser.parse_args()


def start_game(args):
    players = [Player('Player {}'.format(index)) for index in range(args.players)]
    players.append(CliPlayer('myself'))
    game = Game(players)
    game.start()


def main():
    start_game(parse_args())


if __name__ == '__main__':
    main()
