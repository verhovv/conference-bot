from aiogram import Bot
from aiogram.types import FSInputFile

from bot.core.texts import TextEnum, get_text
from web.panel.models import Text, User


async def message_process(
        bot: Bot, chat_id: int, text_enum: TextEnum, user: User, edit=False, message_id=0,
        reply_markup=None
):
    text = await Text.objects.aget(name=text_enum)

    if not text.file:
        if not edit:
            await bot.send_message(
                chat_id=chat_id,
                text=await get_text(text_enum=text_enum, user=user),
                reply_markup=reply_markup
            )
        else:
            await bot.edit_message_text(
                chat_id=chat_id,
                text=await get_text(text_enum=text_enum, user=user)
            )
        return

    media = text.file_id or FSInputFile(path=text.file.path)

    if edit:
        await bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=media,
            reply_markup=reply_markup
        )
        return

    if text.file_type == 'photo':
        msg = await bot.send_photo(
            chat_id=chat_id,
            photo=media,
            caption=await get_text(text_enum=text_enum, user=user),
            reply_markup=reply_markup
        )
        text.file_id = msg.photo[-1].file_id
    elif text.file_type == 'video':
        msg = await bot.send_video(
            chat_id=chat_id,
            video=media,
            caption=await get_text(text_enum=text_enum, user=user),
            reply_markup=reply_markup
        )
        text.file_id = msg.video.file_id
    elif text.file_type == 'document':
        msg = await bot.send_document(
            chat_id=chat_id,
            document=media,
            caption=await get_text(text_enum=text_enum, user=user),
            reply_markup=reply_markup
        )
        text.file_id = msg.document.file_id

    await text.asave()
