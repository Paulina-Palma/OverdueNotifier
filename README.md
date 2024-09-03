# termin_oddania_ksiazki

## Project Overview

This project aims to automate sending email reminders to borrowers who have overdue books. It includes functionalities for database management, fetching borrower details, and sending emails securely.

## Key Components

1. Database Management:

* __Database Class__: Manages SQLite database connections and transactions.
* __Setup Function__: Creates the borrows table if it doesn’t exist.

2. Data Retrieval:

* __get_borrowers_by_return_date Function__: Fetches borrowers with overdue books based on the return date.

3. Email Sending:

* __EmailSender Class__: Manages SMTP connections for sending emails, supporting both SSL and non-SSL connections.
* __send_reminder_to_borrowers Function__: Sends a reminder email to each borrower.
