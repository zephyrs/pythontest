import sqlite3


def create_db(db_name=':memory:'):
    connection = sqlite3.connect(db_name)
    connection.execute('DROP TABLE IF EXISTS teams;')
    connection.execute('''CREATE TABLE teams(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
        );''')
    teams = [('Italy', ), ('France', )]
    with connection:
        connection.executemany('INSERT INTO teams(name) VALUES(?)', teams)
    for row in connection.execute('SELECT id, name FROM teams'):
        print(row)

    connection.execute('DROP TABLE IF EXISTS players;')
    connection.execute('''CREATE TABLE players(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        number INTEGER,
        is_keeper INTEGER,
        skill INTEGER,
        team_id INTERGER,
        FOREIGN KEY(team_id) REFERENCES teams(id) ON DELETE CASCADE
        );''')
    players = [
        ('Gianluigi Buffon', 1, 1, 95, 1),
        ('Gianluca Zambrotta', 13, 0, 88, 1), ('Fabio Cannavaro', 5, 0, 92, 1),
        ('Marco Materazzi', 23, 0, 86, 1), ('Fabio Grosso', 3, 0, 83, 1),
        ('Mauro Camoranesi', 16, 0, 83, 1), ('Gennaro Gattuso', 8, 0, 88, 1),
        ('Andrea Pirlo', 21, 0, 89, 1), ('Simone Perrotta', 20, 0, 80, 1),
        ('Francesco Totti', 10, 0, 92, 1), ('Luca Toni', 9, 0, 87, 1),
        ('Daniele De Rossi', 4, 0, 87, 1), ('Vincenzo Iaquinta', 15, 0, 82, 1),
        ('Alessandro Del Piero', 7, 0, 90, 1),
        ('Fabien Barthez', 16, 1, 86, 2), ('Willy Sagnol', 19, 0, 85, 2),
        ('Lilian Thuram', 15, 0, 90, 2), ('William Gallas', 5, 0, 84, 2),
        ('Eric Abidal', 3, 0, 89, 2), ('Patrick Vieira', 4, 0, 93, 2),
        ('Claude Makelele', 6, 0, 91, 2), ('Franck Ribery', 22, 0, 90, 2),
        ('Zinedine Zidane', 10, 0, 95, 2), ('Florent Malouda', 7, 0, 83, 2),
        ('Thierry Henry', 14, 0, 94, 2), ('Alou Diarra', 18, 0, 81, 2),
        ('David Trezeguet', 20, 0, 88, 2), ('Sylvain Wiltord', 11, 0, 84, 2)
    ]
    with connection:
        connection.executemany(
            'INSERT INTO players(name, number, is_keeper, skill, team_id) VALUES(?, ?, ?, ?, ?)',
            players)
    for row in connection.execute('SELECT * FROM players'):
        print(row)


if __name__ == "__main__":
    create_db('players.db')