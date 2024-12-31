from aiogram import Router, F
from aiogram.types import Message, BotCommand
from aiogram.filters import CommandStart, Command, or_f
from aiogram.fsm.context import FSMContext

from src import bot


router = Router()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
        await message.answer(text="Send me a message, and I will forward it anonymously to OpenSpace. Please, keep your message concise.")
