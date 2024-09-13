import pymysql


class Database:
    def __init__(self, db_name, db_password, db_user, db_port, db_host):
        self.db_name = db_name
        self.db_password = db_password
        self.db_user = db_user
        self.db_port = db_port
        self.db_host = db_host

    def connect(self):
        return pymysql.Connection(
            database=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            cursorclass=pymysql.cursors.DictCursor
        )

    def execute(self, sql: str, params: tuple = (), commit=False, fetchone=False, fetchall=False) -> dict | list:
        database = self.connect()
        cursor = database.cursor()

        cursor.execute(sql, params)
        data = None

        if fetchone:
            data = cursor.fetchone()

        elif fetchall:
            data = cursor.fetchall()

        if commit:
            database.commit()

        return data

    def drop_users_table(self) -> None:
        """
        Drops users table
        """
        sql = """
            DROP TABLE users
        """
        self.execute(sql)

    def create_users_table(self) -> None:
        """
        Creates uses table
        """
        sql = """
            CREATE TABLE IF NOT EXISTS users(
                id INT PRIMARY KEY AUTO_INCREMENT,
                telegram_id BIGINT UNIQUE NOT NULL,
                full_name VARCHAR(100),
                username VARCHAR(100),
                phone_number VARCHAR(13),
                lang VARCHAR(2),
                is_subscribed INT DEFAULT 0
            )
        """
        self.execute(sql)

    def register_user(self, telegram_id: int, full_name: str, username: str, lang: str) -> None:
        """Registers user in a database

        Args:
            telegram_id (int): User's telegram id
            full_name (str): User's full name brought from telegram API
            username (str): User's username brought from telegram API
            lang (str): User's language that was selected from languages menu
        """
        sql = """
            INSERT INTO users(telegram_id, full_name, username, lang)
            VALUES (%s, %s, %s, %s)
        """
        self.execute(sql, (telegram_id, full_name,
                     username, lang), commit=True)

    def get_user(self, telegram_id: int) -> dict:
        """Returns user object from database based on telegram id

        Args:
            telegram_id (int): User's telgram id from telgram API

        Returns:
            dict: User object
        """
        sql = """
            SELECT * FROM users WHERE telegram_id = %s
        """
        return self.execute(sql, (telegram_id,), fetchone=True)

    def get_user_lang(self, telgeram_id: int) -> str:
        """Returns user's selected language from database

        Args:
            telegram_id (int): User's telegram id from telegram API

        Returns:
            str: User's language
        """
        sql = """
            SELECT lang FROM users WHERE telegram_id = %s
        """
        return self.execute(sql, (telgeram_id,), fetchone=True)
