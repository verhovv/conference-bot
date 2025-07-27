from aiogram import Router, Bot, F
from aiogram.types import Message

from bot.core import keyboards
from bot.core.keyboards import CallbackData
from bot.core.texts import TextEnum
from bot.core.utils import message_process
from web.panel.models import User

router = Router()


@router.callback_query(F.data == CallbackData.information)
async def information(callback: Message, user: User, bot: Bot):
    await message_process(
        bot=bot,
        user=user,
        chat_id=callback.from_user.id,
        text_enum=TextEnum.information,
        reply_markup=await keyboards.main_menu_kb(user=user)
    )
