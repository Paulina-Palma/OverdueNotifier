import sqlite3
import pytest
from borrowers import get_borrowers_by_return_date

@pytest.fixture
def create_connection():
    connection = sqlite3.connect(':memory:')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE borrows(
                id INTEGER primary key autoincrement,
                name TEXT,
                email TEXT,
                book_title TEXT,
                book_return_at DATE)''')
    sample_data = [
        (1, 'Adam', 'adam@gmail.com', 'Biblia Excela', '2020-11-12'),
        (2, 'Paula', 'paula@gmail.com', 'Atlas anatomiczny', '2020-12-12'),
        (3, 'Ala', 'ala@gmail.com', 'Programowanie w Pythonie', '2019-11-12')
    ]

    cursor.executemany('INSERT INTO borrows VALUES (?, ?, ?, ?, ?)', sample_data)

    return connection


def test_borrows_test(create_connection):
    borrowers = get_borrowers_by_return_date(create_connection, '2020-12-12')
    assert len(borrowers) == 2
    assert borrowers[0].name == 'Adam'
    assert borrowers[1].name == 'Ala'
