class ScoreBoard(object):
    """
    A class that keeps track of scores for different
    players.
    """
    def __init__(self, names):
        """
        Initializes a Score Board with the given names.
        Scores are initally set to zero.
        """
        self._names = names
        self._values = {}
        self.reset_scores()

    def __str__(self):
        """
        String representation of ScoreBoard object.
        """
        return str(self._values)

    def reset_scores(self, starting_value=0):
        """
        Overwrites the score for each players to
        givern starting_value.
        """
        for name in self._names:
            self.set_score(name, 0)

    def increment_score(self, name, increment):
        """
        Increments the score of player with the given name
        by the given increment.
        """
        self._values[name] += increment

    def reduce_score(self, name, decrement):
        """
        Decrements the score of player with the given name
        by the given decrement.
        """
        self._values[name] -= decrement

    def set_score(self, name, value):
        """
        Sets the score of the player with the give name
        to the given value.
        """
        self._values[name] = value

    def get_score(self, name):
        """
        Returns the current score for the given player.
        """
        return self._values[name]

    def get_winner(self):
        """
        Returns the name of player with highest score.
        """
        return max(self._values.items(), key=lambda x: x[-1])[0]
