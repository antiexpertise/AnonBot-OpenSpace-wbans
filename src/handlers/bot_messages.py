from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, or_f
import hashlib, os
import sqlite3

router = Router()

db_path = '/app/db/bans.db'

open_space_chat ="CHANGE_CHAT_ID_HERE"
@router.message(
    F.content_type.in_(
        [
            "text", "audio", "voice",
            "sticker", "document", "photo",
            "video"
        ]
    ), F.chat.type.in_({"private"})
)

async def echo(message: Message, state:FSMContext) -> None:
    try:
        reply = None
        userHash = getUserHash(message.from_user.id)
        if await isBanned(userHash):
            await message.answer("🚫 nah, man, we chillin")
            return
        if message.content_type == "text":
            reply = None
            if message.reply_to_message:
                if message.reply_to_message.from_user.id == message.from_user.id:
                    reply = message.reply_to_message.message_id + 1
                else:
                    reply = message.reply_to_message.message_id - 1

            await message.bot.send_message(
                open_space_chat,
                message.text,
                entities=message.entities,
                reply_to_message_id=reply,
                parse_mode=None
            )
        if message.content_type == "photo":
            await message.bot.send_photo(
                open_space_chat,
                message.photo[-1].file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                parse_mode=None,
            )
        if message.content_type == "audio":
            await message.bot.send_audio(
                open_space_chat,
                message.audio.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                parse_mode=None
            )
        if message.content_type == "voice":
            await message.bot.send_voice(
                open_space_chat,
                message.voice.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                parse_mode=None
            )
        if message.content_type == "document":
            await message.bot.send_document(
                open_space_chat,
                message.document.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                parse_mode=None
            )
        if message.content_type == "sticker":
            await message.bot.send_sticker(
                open_space_chat,
                message.sticker.file_id
            )
        if message.content_type == "video":
            await message.bot.send_video(
                open_space_chat,
                message.video.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                parse_mode=None,
            )
        await message.bot.send_message(
            open_space_chat,
            "🔼 User Hash: " + str(userHash),
            parse_mode=None
        )
    except Exception as e:
        pass

async def isBanned(userHash: str) -> bool:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM fade WHERE userHash = ?;", (userHash,))
    result = c.fetchone()
    conn.close()
    return result is not None

def getUserHash(userID: int) -> str:
    enter = str(userID)
    sha256_hash = hashlib.sha256()
    sha256_hash.update(enter.encode('utf-8'))
    return sha256_hash.hexdigest()
