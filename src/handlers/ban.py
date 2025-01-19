from aiogram import Router, F
from aiogram.types import Message, BotCommand
from aiogram.filters import CommandStart, Command, or_f
from aiogram.fsm.context import FSMContext
import hashlib
import sqlite3

router = Router()
db_path = '/app/db/bans.db'

@router.message(Command('ban'))
async def start(message: Message, state: FSMContext) -> None:
    if message.chat.type == 'private':
        if message.from_user.id == "CHANGE_ADMIN_ID_HERE":
            user_id = message.text.split()[1]
            await addBan(user_id)
            await message.answer(f"User {user_id} has been banned.")
        else:
            await message.answer("No speako espanol.")

async def addBan(userHash: str):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO fade (userHash) VALUES (?);", (userHash,))
    conn.commit()
    conn.close()



