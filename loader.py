import json

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums.parse_mode import ParseMode

from config import TOKEN, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from utils.db_api.db import Database

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

db = Database(db_name=DB_NAME,
              db_user=DB_USER,
              db_password=DB_PASSWORD,
              db_host=DB_HOST,
              db_port=DB_PORT)

# db.drop_users_table()
# db.drop_categories_table()
# db.drop_lessons_table()
# db.drop_lessons_dataset_table()  # TODO: DOES NOT EXIST YET !!!
db.create_users_table()
db.create_categories_tables()
db.create_lessons_table()
db.create_lessons_dataset_table()


# db.export_to_json("database.json")
# db.load_data_from_json(json_data=json.load(open("database.json", encoding="UTF-8")))
