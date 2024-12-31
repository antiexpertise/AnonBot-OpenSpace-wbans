from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext



router = Router()

open_space_chat ="-1002274331385"

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
    except Exception as e:
        pass