from enum import StrEnum, unique, auto

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.core.texts import get_text, TextEnum
from web.panel.models import User, JobTitle, Contact, Schedule, Activity, Section, FAQ


@unique
class CallbackData(StrEnum):
    back_to_menu = auto()
    information = auto()
    contacts = auto()
    schedule = auto()
    map = auto()
    memo = auto()
    support = auto()
    FAQ = auto()
    change_lang = auto()
    section = auto()
    activity = auto()


async def main_menu(user: User):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=await get_text(text_enum=TextEnum.information_button, user=user),
                    callback_data=CallbackData.information
                ),
                InlineKeyboardButton(
                    text=await get_text(text_enum=TextEnum.contact_button, user=user),
                    callback_data=CallbackData.contacts
                )
            ],
            [
                InlineKeyboardButton(
                    text=await get_text(text_enum=TextEnum.schedule_button, user=user),
                    callback_data=CallbackData.schedule
                ),
                InlineKeyboardButton(
                    text=await get_text(text_enum=TextEnum.map_button, user=user),
                    callback_data=CallbackData.map
                )
            ],
            [
                InlineKeyboardButton(
                    text=await get_text(text_enum=TextEnum.memo_button, user=user),
                    callback_data=CallbackData.memo
                ),
                InlineKeyboardButton(
                    text=await get_text(text_enum=TextEnum.chat_button, user=user),
                    url=await get_text(text_enum=TextEnum.chat_link, user=user)
                )
            ],
            [
                InlineKeyboardButton(
                    text=await get_text(text_enum=TextEnum.faq_button, user=user),
                    callback_data=CallbackData.FAQ
                ),
                InlineKeyboardButton(
                    text=await get_text(text_enum=TextEnum.support_button, user=user),
                    callback_data=CallbackData.support
                )
            ],
            [
                InlineKeyboardButton(
                    text=await get_text(text_enum=TextEnum.lang_button, user=user),
                    callback_data=CallbackData.change_lang
                )
            ],
        ]
    )


async def map(user: User):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=await get_text(text_enum=TextEnum.section_button, user=user),
                    callback_data=CallbackData.section
                )
            ],
            [
                InlineKeyboardButton(
                    text=await get_text(text_enum=TextEnum.activity_button, user=user),
                    callback_data=CallbackData.activity
                )
            ],
            [await main_menu_button(user=user)]
        ]
    )


async def faq_list(user: User):
    keyboard = []

    async for f in FAQ.objects.all():
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f.ru_question if not user.lang else f.en_question,
                    callback_data=f'faq_{f.id}'
                )
            ]
        )

    keyboard.append([await main_menu_button(user)])
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


async def section_list(user: User):
    keyboard = []

    async for s in Section.objects.all():
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=s.ru_name if not user.lang else s.en_name,
                    callback_data=f'section_{s.id}'
                )
            ]
        )
    keyboard.append([
        InlineKeyboardButton(
            text=await get_text(text_enum=TextEnum.back_button, user=user),
            callback_data=CallbackData.map
        )
    ])
    keyboard.append([await main_menu_button(user)])
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


async def section(user: User):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=await get_text(text_enum=TextEnum.back_button, user=user),
                    callback_data=CallbackData.section
                )
            ],
            [await main_menu_button(user)]
        ]
    )


async def activity_list(user: User):
    keyboard = []

    async for a in Activity.objects.all():
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=a.ru_name if not user.lang else a.en_name,
                    callback_data=f'activity_{a.id}'
                )
            ]
        )

    keyboard.append([
        InlineKeyboardButton(
            text=await get_text(text_enum=TextEnum.back_button, user=user),
            callback_data=CallbackData.map
        )
    ])
    keyboard.append([await main_menu_button(user)])
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


async def activity(user: User):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=await get_text(text_enum=TextEnum.back_button, user=user),
                    callback_data=CallbackData.activity
                )
            ],
            [await main_menu_button(user)]
        ]
    )


async def schedule_list(user: User):
    keyboard = []

    async for s in Schedule.objects.all():
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=s.ru_name if not user.lang else s.en_name,
                    callback_data=f'schedule_{s.id}'
                )
            ]
        )

    keyboard.append([await main_menu_button(user)])
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


async def schedule(user: User):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=await get_text(text_enum=TextEnum.back_button, user=user),
                    callback_data=CallbackData.schedule
                )
            ],
            [await main_menu_button(user)]
        ]
    )


async def job_title(user: User):
    keyboard = []

    async for jt in JobTitle.objects.all():
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=jt.ru_name if not user.lang else jt.en_name,
                    callback_data=f'job_{jt.id}'
                )
            ]
        )

    keyboard.append([await main_menu_button(user)])
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


async def contacts(user: User, job_title_id: int):
    keyboard = []

    async for contact in Contact.objects.filter(job_title_id=job_title_id):
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=contact.ru_fio if not user.lang else contact.en_fio,
                    callback_data=f'contact_{contact.id}'
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text=await get_text(text_enum=TextEnum.back_button, user=user),
                callback_data=CallbackData.contacts
            )
        ]
    )

    keyboard.append([await main_menu_button(user)])

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


async def main_menu_button(user: User):
    return InlineKeyboardButton(
        text=await get_text(text_enum=TextEnum.main_menu_button, user=user),
        callback_data=CallbackData.back_to_menu
    )


async def main_menu_kb(user: User):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [await main_menu_button(user)]
        ]
    )
