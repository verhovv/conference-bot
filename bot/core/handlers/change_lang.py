from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery

from bot.core import keyboards
from bot.core.keyboards import CallbackData
from bot.core.texts import TextEnum, get_text
from bot.core.utils import message_process
from web.panel.models import User

router = Router()


@router.callback_query(F.data == CallbackData.change_lang)
async def change_lang(callback: CallbackQuery, user: User, bot: Bot):
    user.lang = not user.lang
    await user.asave()

    try:
        await callback.message.edit_text(
            text=await get_text(text_enum=TextEnum.main_menu, user=user),
            reply_markup=await keyboards.main_menu(user=user)
        )
    except:
        await callback.message.answer(
            text=await get_text(text_enum=TextEnum.main_menu, user=user),
            reply_markup=await keyboards.main_menu(user=user)
        )
