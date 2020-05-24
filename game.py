class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def both_went(self):
        return self.p1Went and self.p2Went

    def winner(self):

        p1 = self.moves[0].upper()[:2]
        p2 = self.moves[1].upper()[:2]

        if p1 == "CH" and p2 == "CO":
            winner = 3
        elif p1 == "CH" and p2 == "CH":
            winner = 0
        elif p1 == "CO" and p2 == "CO":
            winner = 2
        elif p1 == "CO" and p2 == "CH":
            winner = -1

        return winner

    def reset_went(self):
        self.p1Went = False
        self.p2Went = False
