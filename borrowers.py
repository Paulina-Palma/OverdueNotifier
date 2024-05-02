from collections import namedtuple
from data_base import Database

Entity = namedtuple('Entity', 'name email book_title book_return_at')


def get_borrowers_by_return_date(connection, book_return_at):
    entities = []
    with Database(connection) as database:
        database.cursor.execute('''SELECT 
            name, 
            email,
            book_title, 
            book_return_at 
        FROM borrows
        WHERE book_return_at < ?''', (book_return_at,))

        for name, email, book_title, book_return_at in database.cursor.fetchall():
            entities.append(Entity(name, email, book_title, book_return_at))
    return entities
