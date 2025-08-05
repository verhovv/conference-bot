from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart
from bot.core import keyboards
from bot.core.keyboards import CallbackData

from web.panel.models import User, Text
from bot.core.texts import TextEnum, get_text

from .change_lang import router as change_lang_router
from .contacts import router as contacts_router
from .information import router as information_router
from .schedule import router as schedule_router
from .support import router as support_router
from .map import router as map_router
from .memo import router as memo_router
from .faq import router as faq_router
from .sections import router as sections_router

router = Router()
router.include_routers(
    change_lang_router,
    contacts_router,
    information_router,
    schedule_router,
    support_router,
    map_router,
    memo_router,
    faq_router,
    sections_router
)


@router.callback_query(F.data == CallbackData.back_to_menu)
@router.message(CommandStart())
async def command_start(message: Message, user: User, bot: Bot):
    if isinstance(message, CallbackQuery):
        message = message.message
    else:
        await message.delete()

    await message.answer(
        text=await get_text(text_enum=TextEnum.main_menu, user=user),
        reply_markup=await keyboards.main_menu(user=user)
    )
