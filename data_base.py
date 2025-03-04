class Database:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = None

    def __enter__(self):
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()

        if self.cursor:
            self.cursor.close()

        self.connection.close()

