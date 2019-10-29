SYMBOL_SCORE = 'o'
SYMBOL_MISS = 'x'
DEFAULT_PLAY_ROUNDS = 5


class Shooter(object):
    def __init__(self, name, players):
        self._record = []
        self._name = name
        self._players = players

    def display_result(self):
        output = [self._name + ': ']
        for x in self._record:
            output.append(x + ' ')

        i = DEFAULT_PLAY_ROUNDS - len(self._record)
        while i > 0:
            output.append('- ')
            i -= 1
        print(''.join(output))

    def shoot(self, scored):
        self._record.append(SYMBOL_SCORE if scored else SYMBOL_MISS)

    @property
    def score(self):
        return self._record.count(SYMBOL_SCORE)

    @property
    def round(self):
        return len(self._record)

    @property
    def name(self):
        return self._name

    @property
    def keeper_name(self):
        return self._players[0][0]

    @property
    def keep_skill(self):
        return self._players[0][1]

    @property
    def taker_name(self):
        return self._players[len(self._record) + 1][0]

    @property
    def taker_skill(self):
        return self._players[len(self._record) + 1][1]


class PlayerShooter(Shooter):
    def __init__(self, players):
        super(PlayerShooter, self).__init__('YOU', players)


class ComputerShooter(Shooter):
    def __init__(self, players):
        super(ComputerShooter, self).__init__('COM', players)