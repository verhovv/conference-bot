from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from bot.core import keyboards
from bot.core.keyboards import CallbackData
from bot.core.texts import TextEnum
from bot.core.utils import message_process
from web.panel.models import User

router = Router()


@router.callback_query(F.data == CallbackData.memo)
async def memo(callback: CallbackQuery, user: User, bot: Bot):
    await message_process(
        bot=bot,
        chat_id=callback.from_user.id,
        user=user,
        text_enum=TextEnum.memo,
        reply_markup=await keyboards.main_menu_kb(user=user)
    )
