from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from bot.core import keyboards
from bot.core.keyboards import CallbackData
from bot.core.texts import TextEnum, get_text
from web.panel.models import User, Schedule, FAQ

router = Router()


@router.callback_query(F.data == CallbackData.FAQ)
async def faq_list(callback: CallbackQuery, user: User):
    await callback.message.answer(
        text=await get_text(text_enum=TextEnum.schedule, user=user),
        reply_markup=await keyboards.faq_list(user=user)
    )


@router.callback_query(F.data.startswith('faq_'))
async def faq(callback: Message, user: User):
    *_, faq_id = callback.data.split('_')
    faq_id = int(faq_id)

    faq = await FAQ.objects.aget(id=faq_id)

    await callback.message.answer(
        text=faq.ru_answer if not user.lang else faq.en_answer,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=await get_text(text_enum=TextEnum.back_button, user=user),
                        callback_data=CallbackData.FAQ
                    )
                ],
                [await keyboards.main_menu_button(user=user)]
            ]
        )
    )
