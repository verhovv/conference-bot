from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from bot.core import keyboards
from bot.core.keyboards import CallbackData
from bot.core.texts import TextEnum, get_text
from bot.core.utils import message_process
from web.panel.models import User, Section, Schedule, Contact

router = Router()


@router.callback_query(F.data == CallbackData.section)
async def on_section_list(callback: CallbackQuery, user: User, bot: Bot):
    await message_process(
        bot=bot,
        user=user,
        text_enum=TextEnum.section,
        reply_markup=await keyboards.section(user=user)
    )


@router.callback_query(F.data.startswith('section'))
async def on_section(callback: CallbackQuery, user: User, bot: Bot):
    *_, s_id = callback.data.split('_')
    section = await Section.objects.aget(id=int(s_id))

    await callback.message.answer(
        text=section.ru_description if not user.lang else section.en_description,
        reply_markup=await keyboards.c_section(user=user, s=section)
    )


@router.callback_query(F.data.startswith('sec_sch_'))
async def on_section(callback: CallbackQuery, user: User, bot: Bot):
    *_, s_id = callback.data.split('_')
    section = await Section.objects.aget(id=int(s_id))

    inline_keyboard = []

    async for schedule in Schedule.objects.filter(section=section):
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=schedule.ru_name if not user.lang else schedule.en_name,
                    callback_data=f'sec_l_sch_{schedule.id}_{s_id}'
                )
            ]
        )

    await callback.message.answer(
        text=section.ru_description if not user.lang else section.en_description,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard + [
                [
                    InlineKeyboardButton(
                        text=await get_text(text_enum=TextEnum.back_button, user=user),
                        callback_data=f'section_{s_id}'
                    )
                ], [await keyboards.main_menu_button(user=user)]
            ]
        )
    )


@router.callback_query(F.data.startswith('sec_l_sch_'))
async def on_section(callback: CallbackQuery, user: User, bot: Bot):
    *_, sch_id, s_id = callback.data.split('_')
    schedule = await Schedule.objects.aget(id=int(sch_id))

    await callback.message.answer(
        text=schedule.ru_description if not user.lang else schedule.en_description,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(
                        text=await get_text(text_enum=TextEnum.back_button, user=user),
                        callback_data=f'sec_sch_{s_id}'
                    )
                ], [await keyboards.main_menu_button(user=user)]
            ]
        )
    )


@router.callback_query(F.data.startswith('sec_lead_'))
async def on_section(callback: CallbackQuery, user: User, bot: Bot):
    *_, s_id = callback.data.split('_')
    section = await Section.objects.aget(id=int(s_id))

    inline_keyboard = []

    async for contact in Contact.objects.filter(section=section):
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=contact.ru_fio if not user.lang else contact.en_fio,
                    callback_data=f'sec_l_lead_{contact.id}_{s_id}'
                )
            ]
        )

    await callback.message.answer(
        text=section.ru_description if not user.lang else section.en_description,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard + [
                [
                    InlineKeyboardButton(
                        text=await get_text(text_enum=TextEnum.back_button, user=user),
                        callback_data=f'section_{s_id}'
                    )
                ], [await keyboards.main_menu_button(user=user)]
            ]
        )
    )


@router.callback_query(F.data.startswith('sec_l_lead_'))
async def on_section(callback: CallbackQuery, user: User, bot: Bot):
    *_, c_id, s_id = callback.data.split('_')
    contact = await Contact.objects.aget(id=int(c_id))

    await callback.message.answer(
        text=(contact.ru_description if not user.lang else contact.en_description) \
             + f'\n\n{contact.number}\n{contact.link}',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(
                        text=await get_text(text_enum=TextEnum.back_button, user=user),
                        callback_data=f'sec_lead_{s_id}'
                    )
                ], [await keyboards.main_menu_button(user=user)]
            ]
        )
    )
