import json
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

    def execute(self, sql: str, params: tuple = (), commit=False, fetchone=False, fetchall=False):
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

    def drop_categories_table(self) -> None:
        """
        Drops categories table
        """
        sql = """
            DROP TABLE users
        """
        self.execute(sql)

    def drop_lessons_table(self) -> None:
        """
        Drops lessons table
        """
        sql = """
            DROP TABLE lessons
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
                last_visited_place TEXT,
                is_subscribed INT DEFAULT 0,
                notifications INT DEFAULT 1,
                homeworks_done VARCHAR(100)
            )
        """
        self.execute(sql)

    def create_categories_tables(self) -> None:
        """
        Creates courses categories table
        """
        sql = """
            CREATE TABLE IF NOT EXISTS categories(
                id INT PRIMARY KEY AUTO_INCREMENT,
                name_uz VARCHAR(200) NOT NULL,
                name_ru VARCHAR(200) NOT NULL,
                name_en VARCHAR(200) NOT NULL
            )
        """
        self.execute(sql)

    def create_lessons_table(self) -> None:
        """
        Creates lessons table
        """
        sql = """
            CREATE TABLE IF NOT EXISTS lessons(
                id INT PRIMARY KEY AUTO_INCREMENT,
                category_id INT NOT NULL,
                title_uz VARCHAR(100),
                title_ru VARCHAR(100),
                title_en VARCHAR(100),
                file_id VARCHAR(255),
                payment_required INT NOT NULL
            )
        """
        self.execute(sql)

    def create_lessons_dataset_table(self) -> None:
        """
        Creates a table where a dataset of lessons is stored that contains which lesson is opened for which people
        """
        sql = """
            CREATE TABLE IF NOT EXISTS lessons_dataset(
                id INT PRIMARY KEY AUTO_INCREMENT,
                lesson_id INT NOT NULL,
                for_users TEXT
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

    def update_last_visited_place(self, last_visited_place: int, telegram_id: int) -> None:
        """Updated last visited section of a user

        Args:
            telegram_id (int): User's telgram id
            last_visited_place (int): Last visited place of a user
        """
        sql = """
            UPDATE users SET last_visited_place = %s WHERE telegram_id = %s
        """
        self.execute(sql, (last_visited_place, telegram_id), commit=True)

    def update_language(self, lang: str, telegram_id: int) -> None:
        """Updates user's language

        Args:
            lang (str): User's selected language
            telegram_id (int): User's telegram id
        """
        sql = """
            UPDATE users SET lang = %s WHERE telegram_id = %s
        """
        self.execute(sql, (lang, telegram_id), commit=True)

    def update_phone_number(self, phone_number: str, telegram_id: int) -> None:
        """Update user's phone number in database

        Args:
            phone_number (str): User's phone number
            telegram_id (int): User's telegram id from telegram API
        """
        sql = """
            UPDATE users set phone_number = %s WHERE telegram_id = %s
        """
        self.execute(sql, (phone_number, telegram_id), commit=True)

    def update_user_homework(self, user_id: int, lesson_id: int):
        """Updates user's homeworks list and inserts new lesson id to completed homeworks ids list
        
        Args:
            user_id: User's id
            lesson_id (int): Lesson's id
        """
        sql = """
            SELECT homeworks_done from users WHERE id = %s
        """
        
        homeworks_done = self.execute(sql, (user_id,), fetchone=True).get('homeworks_done')

        if homeworks_done:
            if str(lesson_id) not in homeworks_done:
                homeworks_done += "," + str(lesson_id)
        else:
            homeworks_done = str(lesson_id)

        sql = """
            UPDATE users SET homeworks_done = %s WHERE id = %s
        """
        self.execute(sql, (homeworks_done, user_id), commit=True)

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

    def get_user_by_id(self, user_id: int) -> dict:
        """Returns user object by user's id

        Args:
            user_id (int): User's id

        Returns:
            dict: User object
        """
        sql = """
            SELECT * FROM users WHERE id = %s
        """
        return self.execute(sql, (user_id,), fetchone=True)

    def get_user_lang(self, telegeram_id: int) -> str:
        """Returns user's selected language from database

        Args:
            telegram_id (int): User's telegram id from telegram API

        Returns:
            str: User's language
        """
        sql = """
            SELECT lang FROM users WHERE telegram_id = %s
        """
        return self.execute(sql, (telegeram_id,), fetchone=True).get("lang")

    def get_categories(self) -> list:
        """Gets all categories from database

        Returns:
            list: List of all categories
        """
        sql = """
            SELECT * FROM categories
        """
        return self.execute(sql, fetchall=True)

    def get_lessons(self, category_id: int) -> list:
        """Returns the list of all lessons by category_id

        Args:
            category_id (int): Lesson's category

        Returns:
            list: List of all courses
        """
        sql = """
            SELECT * FROM lessons where category_id = %s
        """
        return self.execute(sql, (category_id,), fetchall=True)

    def get_lesson(self, lesson_id: int) -> dict:
        """Returns particular lesson by lesson id

        Args:
            lesson_id (int): selected lesson's id

        Returns:
            dict: Lesson object
        """
        sql = """
            SELECT * FROM lessons WHERE id = %s
        """
        return self.execute(sql, (lesson_id,), fetchone=True)

    def get_users_done_homeworks(self, user_id: int) -> str:
        """Returns completed homeworks list of a particular user

        Args:
            user_id (int): user's id

        Returns:
            str: Completed homeworks list
        """
        sql = """
            SELECT homeworks_done FROM users
            WHERE id = %s
        """
        return self.execute(sql, (user_id,), fetchone=True).get('homeworks_done')

    def grant_or_close_access(self, phone_number: str, access: int) -> None:
        """Grants access to a particular user by phone number

        Args:
            phone_number (str): user's phone number
            access (int): access type
        """
        sql = """
            UPDATE users SET is_subscribed = %s
            WHERE phone_number = %s
        """
        self.execute(sql, (access, phone_number), commit=True)

    def export_to_json(self, file_path='data_dump.json'):
        """Exports all tables data to a JSON file"""
        data = {
            "users": self.get_all_records("users"),
            "categories": self.get_all_records("categories"),
            "lessons": self.get_all_records("lessons"),
            "lessons_dataset": self.get_all_records("lessons_dataset")
        }

        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def get_all_records(self, table_name: str) -> list:
        """Gets all records from a table"""
        sql = f"SELECT * FROM {table_name}"
        return self.execute(sql, fetchall=True)

    def insert_user(self, user):
        sql = """
            INSERT INTO users (id, telegram_id, full_name, username, phone_number, lang, last_visited_place, is_subscribed, notifications, homeworks_done)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.execute(sql, (
            user["id"], user["telegram_id"], user["full_name"], user["username"], user["phone_number"],
            user["lang"], user["last_visited_place"], user["is_subscribed"], user["notifications"], user["homeworks_done"]
        ), commit=True)

    def insert_category(self, category):
        sql = """
            INSERT INTO categories (id, name_uz, name_ru, name_en)
            VALUES (%s, %s, %s, %s)
        """
        self.execute(sql, (category["id"], category["name_uz"],
                     category["name_ru"], category["name_en"]), commit=True)

    def insert_lesson(self, lesson):
        sql = """
            INSERT INTO lessons (id, category_id, title_uz, title_ru, title_en, file_id, payment_required)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.execute(sql, (
            lesson["id"], lesson["category_id"], lesson["title_uz"], lesson["title_ru"], lesson["title_en"],
            lesson["file_id"], lesson["payment_required"]
        ), commit=True)

    def insert_lesson_dataset(self, lesson_dataset):
        sql = """
            INSERT INTO lessons_dataset (id, lesson_id, for_users)
            VALUES (%s, %s, %s)
        """
        self.execute(
            sql, (lesson_dataset["id"], lesson_dataset["lesson_id"], lesson_dataset["for_users"]), commit=True)

    def load_data_from_json(self, json_data):
        for user in json_data["users"]:
            self.insert_user(user)

        for category in json_data["categories"]:
            self.insert_category(category)

        for lesson in json_data["lessons"]:
            self.insert_lesson(lesson)

        for lesson_dataset in json_data["lessons_dataset"]:
            self.insert_lesson_dataset(lesson_dataset)
