
import psycopg2

# Postgres configuration
USER = 'gEphephA6eWr'
PASSWORD = 'fUBanasp4fup'
NAME = 'prE8rufr7BUc'
POSTGRES_HOST = 'restfulapi-v2-prod02.ccoyoeut8gty.us-east-1.rds.amazonaws.com'


class PostgresProd:

    def __init__(self):
        self.cursor = None
        self.prod = None

    def open_database(self):
        self.prod = psycopg2.connect(host=POSTGRES_HOST, user=USER, password=PASSWORD, dbname=NAME)
        self.cursor = self.prod.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()

    def commit(self):
        self.prod.commit()
