from aiogram import types

from loader import db
from router import router


@router.message(lambda call: "accept_or_deny_homework" in call.data)
async def accept_or_deny(call: types.CallbackQuery):
    lang = db.get_user_lang(call.from_user.id)
    command = call.data.split(":")[-1]

    if command == "accept":
        ...
    elif command == "deny":
        ...
    