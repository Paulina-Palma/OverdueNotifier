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

ssl_enable = getenv('SSL_ENABLE', 'False').lower() in ['true', '1', 't']
port = int(getenv('PORT', 587))
smtp_server = getenv('SMTP_SERVER')
username = getenv('MAIL_USERNAME')
password = getenv('MAIL_PASSWORD')

subject = getenv('SUBJECT', 'Proszę o pilny zwrot książek')
sender = getenv('SENDER')

credentials = Credentials(username, password)


def setup(connection):
    with Database(connection) as database:
        database.cursor.execute('''CREATE TABLE IF NOT EXISTS borrows(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            book_title TEXT,
            book_return_at DATE)''')


def send_reminder_to_borrowers(connection, borrower):
    template = Template('''
    Dzień dobry $name!
    Pamiętasz, że masz wypożyczoną książkę $title ??!!
    Data zwrotu minęła $book_return_at

    Prosimy o pilny zwrot!
    ''')
    text = template.substitute({
        'name': borrower.name,
        'title': borrower.book_title,
        'book_return_at': borrower.book_return_at
    })

    message = email.message.EmailMessage()
    message.set_content(text)
    message['From'] = sender
    message['To'] = borrower.email
    message['Subject'] = subject

    connection.send_message(message)
    print(f'Wysyłam email do {borrower.email}')


if __name__ == '__main__':
    setup(connection)
    borrowers = get_borrowers_by_return_date(connection, '2024-12-24')
    with EmailSender(port, smtp_server, credentials, ssl_enable) as email_connection:
        for borrower in borrowers:
            try:
                send_reminder_to_borrowers(email_connection, borrower)
            except Exception as e:
                print(f'Failed to send email to {borrower.email}: {e}')