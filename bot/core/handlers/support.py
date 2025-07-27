from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot.core import keyboards
from bot.core.keyboards import CallbackData
from bot.core.texts import TextEnum, get_text
from web.panel.models import User

router = Router()


@router.callback_query(F.data == CallbackData.support)
async def support(callback: CallbackQuery, user: User, bot: Bot):
    await callback.message.answer(
        text=f'{"Контактные данные" if not user.lang else "Contact data"}:\n\n'
             f'{"Телефон" if not user.lang else "Phone"}: {await get_text(text_enum=TextEnum.phone_number, user=user)}',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=await get_text(text_enum=TextEnum.phone_button, user=user),
                        url=await get_text(text_enum=TextEnum.tg_link, user=user)
                    )
                ],
                [await keyboards.main_menu_button(user=user)]
            ]
        )
    )
