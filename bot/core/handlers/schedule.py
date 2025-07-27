from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.core import keyboards
from bot.core.keyboards import CallbackData
from bot.core.texts import TextEnum, get_text
from web.panel.models import User, Schedule

router = Router()


@router.callback_query(F.data == CallbackData.schedule)
async def schedule_list(callback: CallbackQuery, user: User):
    await callback.message.answer(
        text=await get_text(text_enum=TextEnum.schedule, user=user),
        reply_markup=await keyboards.schedule_list(user=user)
    )


@router.callback_query(F.data.startswith('schedule_'))
async def schedule(callback: Message, user: User):
    *_, schedule_id = callback.data.split('_')
    schedule_id = int(schedule_id)

    s = await Schedule.objects.aget(id=schedule_id)

    await callback.message.answer(
        text=s.ru_description if not user.lang else s.en_description,
        reply_markup=await keyboards.schedule(user=user)
    )
