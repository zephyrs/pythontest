r'''
penalty shooting
'''
import random
import sqlite3
from enum import Enum, unique
from shooter import PlayerShooter, ComputerShooter, DEFAULT_PLAY_ROUNDS


@unique
class GameResult(Enum):
    Draw = 0
    PlayerWin = 1
    ComputerWin = 2


class ShootoutGame():
    @staticmethod
    def shuffle_players(player):
        copy = player[1:]
        random.shuffle(copy)
        player[1:] = copy

    def __init__(self):
        pass

    def main(self):
        self._connection = sqlite3.connect('players.db')
        italy_players = self._connection.execute(
            'SELECT players.name, skill FROM players LEFT JOIN teams ON players.team_id = teams.id WHERE teams.name = "Italy"'
        ).fetchall()

        france_players = self._connection.execute(
            'SELECT players.name, skill FROM players LEFT JOIN teams ON players.team_id = teams.id WHERE teams.name = "France"'
        ).fetchall()

        self.shuffle_players(italy_players)
        self.shuffle_players(france_players)

        self.toss_coin()
        shooters = (
            PlayerShooter(italy_players),
            ComputerShooter(france_players)) if self._is_player_right else (
                ComputerShooter(italy_players), PlayerShooter(france_players))

        i = 0
        while True:
            self.shooting_action(shooters[i % 2], shooters[(i + 1) % 2])
            result = self.judge_score(shooters)
            if result != GameResult.Draw:
                print('you win!!!' if result ==
                      GameResult.PlayerWin else 'you lose!!!')
                break
            i += 1

        print('The final score is %d:%d (%d rounds)' %
              (shooters[0].score, shooters[1].score, shooters[0].round))

        shooters[0].display_result()
        shooters[1].display_result()

    def toss_coin(self):
        toss_map = {0: ('h', 'Head'), 1: ('t', 'Tail')}
        player_choise = input(
            'Coin tossing... choose Head(\'h\') or Tail(\'t\')) --> ').rstrip(
            )
        toss_result = random.randrange(2)
        print('Toss result is %s...' % toss_map[toss_result][1])
        self._is_player_right = player_choise == toss_map[toss_result][0]
        if self._is_player_right:
            print('And you win! You will shoot first!')
        else:
            print('Sorry you lose! Computer will shoot first!')

    def shooting_action(self, shooter, keeper):
        direction_list = ['l', 'm', 'r']
        directions_map = {'l': 'left', 'm': 'middle', 'r': 'right'}
        shoot_choise = ''
        keep_choise = ''
        while True:
            print('%s is stepping up to take the penalty...' %
                  shooter.taker_name)
            if (isinstance(shooter, PlayerShooter)):
                shoot_choise = input(
                    'Your shooting turn... choose from (\'l\', \'m\', \'r\') --> '
                ).rstrip()
                keep_choise = random.choice(direction_list)
            else:
                keep_choise = input(
                    'Your saving turn... choose from (\'l\', \'m\', \'r\') --> '
                ).rstrip()
                shoot_choise = random.choice(direction_list)
            if keep_choise in direction_list and shoot_choise in direction_list:
                break
            print('Invalid input... Do it again!')

        msg = ''
        scored = True
        if shoot_choise != keep_choise:
            odds = random.randint(0, 99)
            print("shoot skill vs odds -> %d vs %d" %
                  (shooter.taker_skill, odds))
            if shooter.taker_skill < odds:
                scored = False
                msg = 'MISSED! ' + random.choice([
                    'He sends it wide!', 'He hits the crossbar!',
                    'Hit the post... and bounces out!',
                    'He sends his kick high over the bar!', 'WAY HIGH!'
                ])
            else:
                msg = 'SCORED! ' + random.choice([
                    'He sends the keeper the wrong way!',
                    'He makes no mistake!', 'What a confident strike!',
                    'He powers his penalty straight into the net!',
                    'No chance for the keeper!'
                ])
        else:
            odds_shooter = random.uniform(0.8, 1.0)
            odds_keeper = random.uniform(0.8, 1.0)
            print("shooter vs keeper -> %d(%d, %f) vs %d(%d, %f)" %
                  (shooter.taker_skill * odds_shooter, shooter.taker_skill,
                   odds_shooter, keeper.keep_skill * odds_keeper,
                   keeper.keep_skill, odds_keeper))
            if shooter.taker_skill * odds_shooter < keeper.keep_skill * odds_keeper:
                scored = False
                msg = 'SAVED! ' + random.choice([
                    'The keeper reaches the ball... What a finger-tip save!',
                    'The keeper parries it wide of the post!',
                    'The keeper saves with his legs!',
                    'The keeper leaps right and punches it away!',
                    'He strikes a poor effort at goal, allowing the keeper to make the stop.'
                ])
            else:
                msg += 'SCORED! ' + random.choice([
                    'Although the keeper guessed right...',
                    'The keeper dives the right way but he cannot reach it...',
                    'The keeper gets a hand to the ball but there\'s too much power for him!',
                    'That was just about unstoppable.',
                    'In off the post! Some good fortune for the striker!'
                ])

        print('\t%s shoot to %s, %s save to %s... %s' %
              (shooter.taker_name, directions_map[shoot_choise],
               keeper.keeper_name, directions_map[keep_choise], msg))
        shooter.shoot(scored)

    @staticmethod
    def judge_score(s):
        s1, s2 = s[0], s[1]
        print('(Round %d)    %s:%s - %d:%d' %
              (s1.round, s1.name, s2.name, s1.score, s2.score))
        player, com = s1, s2
        if isinstance(s1, ComputerShooter):
            player, com = s2, s1

        if player.round < DEFAULT_PLAY_ROUNDS:
            if player.score > DEFAULT_PLAY_ROUNDS - com.round + com.score:
                return GameResult.PlayerWin
            elif com.score > DEFAULT_PLAY_ROUNDS - player.round + player.score:
                return GameResult.ComputerWin
        elif player.round > DEFAULT_PLAY_ROUNDS:
            if player.round == com.round:
                if player.score > com.score:
                    return GameResult.PlayerWin
                elif player.score < com.score:
                    return GameResult.ComputerWin
        else:
            if player.round >= com.round:
                if player.score > DEFAULT_PLAY_ROUNDS - com.round + com.score:
                    return GameResult.PlayerWin
                elif com.score > DEFAULT_PLAY_ROUNDS - player.round + player.score:
                    return GameResult.ComputerWin
        return GameResult.Draw


if __name__ == "__main__":
    ShootoutGame().main()
