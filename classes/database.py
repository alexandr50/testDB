import psycopg2



class DBManager:

    def __init__(self, name_bd: str, params: dict):
        self.name_db = name_bd
        self.params = params

    def create_database(self):
        """Метод создания базы данных и двух таблиц"""
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute(f"""DROP DATABASE IF EXISTS {self.name_db}""")
            cur.execute(f"""CREATE DATABASE {self.name_db}""")