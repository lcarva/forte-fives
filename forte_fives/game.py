import deck
import hand
import scoreboard
import rules


class Game(object):
    """
    This class represents an instance of a 45s game.
    """

    def __init__(self, players):
        """
        Initializes a game with the given players.
        """
        self.players = players
        # Initialize the score board.
        self.score_board = scoreboard.ScoreBoard(
            [p.name for p in self.players])

    def start(self):
        """
        Starts the game.
        """
        print "Welcome to Forte Fives!"
        print

        # Should break out of loop, when one of the players
        # hits the high score of 120.
        while self.should_continue():
            self.play_round()

        # TODO: Determine the winner of the game.

    def should_continue(self):
        """
        Determines if the game should continue or not.
        """
        for player in self.players:
            if self.score_board.get_score(player.name) > rules.WINNING_SCORE:
                return False
        return True

    def play_round(self):
        """
        Plays a round.
        """

        # Create a deck of cards and shuffle it.
        self.deck = deck.Deck()
        self.deck.shuffle()

        # Deal cards and create kiddie.
        kiddie = self.deal_cards()

        # Keep track of the winning players and their cards.
        winners = []

        for player in self.players:
            print player, ':', player.hand
        print 'Kiddie', ':', kiddie

        # Start bidding process.
        bidding_player, current_bid = self.start_bidding()
        # Store the initial score to determine later if player made bid.
        bp_initial_score = self.score_board.get_score(bidding_player.name)

        # Determine the playing suit.
        playing_suit = bidding_player.select_suit()
        print 'Player %s has selected %s suit' % (bidding_player, playing_suit)

        # Initialize the starting player to bidder.
        starting_player = bidding_player

        # Give starting player the kiddie.
        for c in kiddie:
            starting_player.hand.add_card(c)

        # Allow players to throw out cards and get new cards.
        # Determine the order of the players.
        index = self.players.index(starting_player)
        ordered_players = self.players[index:] + self.players[:index]
        self.improve_cards(ordered_players, playing_suit)

        # Actually start playing!
        # 5 is the number of cards on each hand.
        for x in range(5):
            print "Starting player is", starting_player
            starting_player, winning_card = self.play_hand(starting_player,
                                                           playing_suit,
                                                           current_bid)
            winners.append((starting_player, winning_card))

        # Give the player with the highest card an additional 5 points.
        cards = [c for p, c in winners]
        highest_card = rules.get_highest_card_in_suit(playing_suit, cards)
        for p, c in winners:
            if c == highest_card:
                self.score_board.increment_score(p.name, 5)
                print p, 'had the highest card', c
                print 'Current score:'
                print self.score_board
                break

        # If bidding player didn't make bid, deduct the bid.
        bp_current_score = self.score_board.get_score(bidding_player.name)
        if bp_current_score - current_bid < bp_initial_score:
            print bidding_player, 'did NOT make his bid.'
            print ("Score before the adjustment: %d" %
                   self.score_board.get_score(bidding_player.name))
            self.score_board.set_score(bidding_player.name,
                                       bp_initial_score - current_bid)
            print ("Score after the adjustment: %d" %
                   self.score_board.get_score(bidding_player.name))

    def start_bidding(self):
        """
        Each player has one chance to bid. After all player have
        placed a bid, the highest bid wins. Since a new bid can only
        be higher than the previous bid, the latest bid is also
        the highest bid.
        """
        current_bid = None
        bidding_player = None
        for player in self.players:
            new_bid = player.place_bid(current_bid)
            if new_bid:
                print player, 'has bid', new_bid
                bidding_player = player
                current_bid = new_bid
            else:
                print player, 'passes on bid.'

        # If no players bid, dealer HAS to bid.
        if bidding_player is None:
            bidding_player = self.players[0]
            current_bid = rules.BIDS[0]

        print 'Bidding player is', bidding_player

        return bidding_player, current_bid

    def play_hand(self, starting_player, playing_suit, bid):
        """
        Each player will deal a card, starting with the starting
        player, of course.
        Updates the score for each player.
        Returns the winner player.
        """
        # Determine the order of the players.
        index = self.players.index(starting_player)
        ordered_players = self.players[index:] + self.players[:index]

        # Set a list of cards that have already been played.
        on_table = []
        # Let the game begin!
        for p in ordered_players:
            played_card = p.play_card(playing_suit, on_table)
            print p, "played", played_card
            on_table.append(played_card)
        print "Table:", on_table

        # Determine the winner.
        winning_card = rules.get_winnind_card(playing_suit, on_table)
        index = on_table.index(winning_card)
        # Use the index of the card played to match the player.
        winner = ordered_players[index]
        print 'Winner is', winner, 'with card', winning_card

        # Update the score board.
        self.score_board.increment_score(winner.name, 5)
        print 'Current score:'
        print self.score_board
        # Return the winner.
        return winner, winning_card

    def deal_cards(self):
        """
        Deal initial cards to each player and kiddie.
        Returns the kiddie.
        """
        # Deal 3 cards to each player.
        for p in self.players:
            p.set_hand(hand.Hand())
            for x in xrange(3):
                p.hand.add_card(self.deck.pick_card())

        # Create kiddie and deal 3 cards to it.
        kiddie = hand.Hand()
        for x in xrange(3):
            kiddie.add_card(self.deck.pick_card())

        # Deal 2 more cards to each player.
        for p in self.players:
            for x in xrange(2):
                p.hand.add_card(self.deck.pick_card())

        return kiddie

    def improve_cards(self, ordered_players, suit):
        """
        Every player gets a chance to throw out their "bad" cards
        and get new cards with the hope of getting better cards.
        """
        for p in ordered_players:
            amount = p.discard_cards(suit)
            print p, 'discarded', amount, 'cards.'
            # Deal new cards.
            for x in range(amount):
                p.hand.add_card(self.deck.pick_card())

if __name__ == '__main__':
    import player
    p1 = player.Player('Bruce Lee')
    p2 = player.Player('John Rambo')
    p3 = player.Player('Van Damme')
    p4 = player.Player('Luiz Carvalho')
    game = Game([p1, p2, p3, p4])
    game.start()
    print "Game over!"
    print "Length of deck is %d" % len(game.deck)
