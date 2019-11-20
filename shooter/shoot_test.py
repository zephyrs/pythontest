import random
import sqlite3
import time
import unittest

from penalty_shoot import GameResult, ShootoutGame
from shooter import ComputerShooter, PlayerShooter


class TestPenaltyCase(unittest.TestCase):
    def test_play(self):
        connection = sqlite3.connect("players.db")
        italy_players = connection.execute(
            'SELECT players.name, skill FROM players LEFT JOIN teams ON players.team_id = teams.id WHERE teams.name = "Italy"'
        ).fetchall()

        france_players = connection.execute(
            'SELECT players.name, skill FROM players LEFT JOIN teams ON players.team_id = teams.id WHERE teams.name = "France"'
        ).fetchall()

        count = 10
        while count > 0:
            print("simlutor test round: %d" % (11 - count))
            ShootoutGame.shuffle_players(italy_players)
            ShootoutGame.shuffle_players(france_players)
            if count % 2:
                shooters = (
                    PlayerShooter(italy_players),
                    ComputerShooter(france_players),
                )
            else:
                shooters = (
                    ComputerShooter(italy_players),
                    PlayerShooter(france_players),
                )
            i = 0
            while True:
                shooters[i % 2].shoot(random.random() > 0.2)
                result = ShootoutGame.judge_score(shooters)
                if result != GameResult.Draw:
                    print(
                        "you win!!!"
                        if result == GameResult.PlayerWin
                        else "you lose!!!"
                    )
                    break
                i += 1
            count -= 1
            print(
                "The final score is %d:%d (%d rounds)"
                % (shooters[0].score, shooters[1].score, shooters[0].round)
            )

            shooters[0].display_result()
            shooters[1].display_result()
            time.sleep(0.2)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPenaltyCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
