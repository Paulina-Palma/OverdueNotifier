import email
from os import getenv
import sqlite3
from string import Template
from dotenv import load_dotenv
from borrowers import get_borrowers_by_return_date
from data_base import Database
from emails import EmailSender, Credentials

load_dotenv()
connection = sqlite3.connect(getenv('DB_NAME'))

ssl_enable = getenv('SSL_ENABLE', False)
port = getenv('PORT')
smtp_server = getenv('SMTP_SERVER')
username = getenv('MAIL_USERNAME')
password = getenv('MAIL_PASSWORD')

subject = getenv('SUBJECT')
sender = getenv('SENDER')

credentials = Credentials(username, password)


def setup(connection):
    with Database(connection) as database:
        database.cursor.execute('''CREATE TABLE borrows(
            id INTEGER primary key autoincrement,
            name TEXT,
            email TEXT,
            book_title TEXT,
            book_return_at DATE)''')


def send_reminder_to_borrowers(borrower):
    template = Template('''
    Hej $name!
    Pamiętasz, że masz moją książkę $title ??!!
    Oddaj mi ją jak najszybciej!
    Data zwrotu minęła $book_return_at

    Czekam!
    ''')
    text = template.substitute({
        'name': borrower.name,
        'title': borrower.book_title,
        'book_return_at': borrower.book_return_at
    })

    message = email.message_from_string(text)

    message.set_charset('utf-8')
    message['From'] = sender
    message['To'] = borrower.email
    message['Subject'] = 'Oddaj mi natychmiast'
    connection.sendmail(sender, borrower.email, message)

    print(f'Wysyłam email do {borrower.email}')


if __name__ == '__main__':
    borrowers = get_borrowers_by_return_date(connection, '2024-12-24')
    with EmailSender(port, smtp_server, credentials) as connection:
        for borrower in borrowers:
            send_reminder_to_borrowers(borrower)
