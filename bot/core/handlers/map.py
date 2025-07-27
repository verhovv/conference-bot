from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery

from bot.core import keyboards
from bot.core.keyboards import CallbackData
from bot.core.texts import TextEnum, get_text
from bot.core.utils import message_process
from web.panel.models import User, Activity, Section

router = Router()


@router.callback_query(F.data == CallbackData.map)
async def map(callback: CallbackQuery, user: User, bot: Bot):
    await message_process(
        bot=bot,
        chat_id=callback.from_user.id,
        user=user,
        text_enum=TextEnum.map,
        reply_markup=await keyboards.map(user=user)
    )


@router.callback_query(F.data == CallbackData.activity)
async def activity_list(callback: Message, user: User):
    await callback.message.answer(
        text=await get_text(text_enum=TextEnum.activity, user=user),
        reply_markup=await keyboards.activity_list(user=user)
    )


@router.callback_query(F.data.startswith('activity_'))
async def activity(callback: Message, user: User):
    *_, activity_id = callback.data.split('_')
    activity_id = int(activity_id)

    a = await Activity.objects.aget(id=activity_id)

    await callback.message.answer(
        text=a.ru_description if not user.lang else a.en_description,
        reply_markup=await keyboards.activity(user=user)
    )


@router.callback_query(F.data == CallbackData.section)
async def section_list(callback: Message, user: User):
    await callback.message.answer(
        text=await get_text(text_enum=TextEnum.section, user=user),
        reply_markup=await keyboards.section_list(user=user)
    )


@router.callback_query(F.data.startswith('section_'))
async def section(callback: Message, user: User):
    *_, section_id = callback.data.split('_')
    section_id = int(section_id)

    s = await Section.objects.aget(id=section_id)

    await callback.message.answer(
        text=s.ru_description if not user.lang else s.en_description,
        reply_markup=await keyboards.section(user=user)
    )
