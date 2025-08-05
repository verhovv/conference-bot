from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile

from bot.core import keyboards
from bot.core.keyboards import CallbackData
from bot.core.texts import TextEnum, get_text
from web.panel.models import User, Schedule, Section
from bot.core.utils import message_process

import datetime

router = Router()


@router.callback_query(F.data == CallbackData.schedule)
async def schedule_mode(callback: CallbackQuery, user: User, bot: Bot):
    await message_process(
        bot=bot,
        user=user,
        chat_id=callback.from_user.id,
        text_enum=TextEnum.schedule,
        reply_markup=await keyboards.schedule_mode(user=user)
    )


@router.callback_query(F.data == CallbackData.schedule_days)
async def schedule_dates(callback: CallbackQuery, user: User):
    await callback.message.answer(
        text=await get_text(text_enum=TextEnum.schedule, user=user),
        reply_markup=await keyboards.schedule_dates(user=user)
    )


@router.callback_query(F.data.startswith('schedule_date_'))
async def schedule_dates_list(callback: CallbackQuery, user: User):
    *_, ordinal_day = callback.data.split('_')
    ordinal_day = int(ordinal_day)

    date = datetime.date.fromordinal(ordinal_day)

    await callback.message.answer(
        text=date.strftime('%d.%m.%Y'),
        reply_markup=await keyboards.schedule_dates_list(user=user, date=date)
    )


@router.callback_query(F.data == CallbackData.schedule_sections)
async def schedule_sections(callback: CallbackQuery, user: User):
    await callback.message.answer(
        text=await get_text(text_enum=TextEnum.schedule, user=user),
        reply_markup=await keyboards.schedule_sections(user=user)
    )


@router.callback_query(F.data.startswith('schedule_section_'))
async def schedule_dates_list(callback: CallbackQuery, user: User):
    *_, section_id = callback.data.split('_')
    section_id = int(section_id)

    section = await Section.objects.aget(id=section_id)

    await callback.message.answer(
        text=section.ru_description if not user.lang else section.en_description,
        reply_markup=await keyboards.schedule_sections_list(user=user, se=section)
    )


@router.callback_query(F.data == CallbackData.schedule)
async def schedule_list(callback: CallbackQuery, user: User):
    await callback.message.answer(
        text=await get_text(text_enum=TextEnum.schedule, user=user),
        reply_markup=await keyboards.schedule_dates(user=user)
    )


@router.callback_query(F.data.startswith('schedule_'))
async def schedule(callback: Message, user: User):
    *_, schedule_id = callback.data.split('_')
    schedule_id = int(schedule_id)

    s = await Schedule.objects.aget(id=schedule_id)

    text = s.ru_description if not user.lang else s.en_description
    reply_markup = await keyboards.schedule(user=user, s=s)

    if not s.file:
        await callback.message.answer(
            text=text,
            reply_markup=reply_markup
        )
        return

    msg = await callback.message.answer_photo(
        photo=FSInputFile(path=s.file.path) if not s.file_id else s.file_id,
        caption=text,
        reply_markup=reply_markup
    )

    if not s.file_id:
        s.file_id = msg.photo[-1].file_id
        await s.asave()
