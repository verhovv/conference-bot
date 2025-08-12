from enum import StrEnum, unique, auto

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime

from asgiref.sync import sync_to_async

from bot.core.texts import get_text, TextEnum
from web.panel.models import User, JobTitle, Contact, Schedule, Section, FAQ


@unique
class CallbackData(StrEnum):
    back_to_menu = auto()
    information = auto()
    contacts = auto()
    schedule = auto()
    schedule_days = auto()
    schedule_sections = auto()
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
                    text=await get_text(text_enum=TextEnum.section_button, user=user),
                    callback_data=CallbackData.section
                )
            ],
            [
                InlineKeyboardButton(
                    text=await get_text(text_enum=TextEnum.tg_channel_button, user=user),
                    url=await get_text(text_enum=TextEnum.tg_channel_link, user=user)
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
                    text=await get_text(text_enum=TextEnum.map_in_button, user=user),
                    url=await get_text(text_enum=TextEnum.map_in_button_link, user=user)
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
        inline_keyboard=
        [[InlineKeyboardButton(
            text=s.ru_name if not user.lang else s.en_name,
            callback_data=f'section_{s.id}'
        )] async for s in Section.objects.all()] \
        + [
            [await main_menu_button(user)]
        ]
    )


async def c_section(user: User, s: Section):
    return InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text=await get_text(text_enum=TextEnum.section_schedule_button, user=user),
                    callback_data=f'sec_sch_{s.id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=await get_text(text_enum=TextEnum.section_leading_button, user=user),
                    callback_data=f'sec_lead_{s.id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=await get_text(text_enum=TextEnum.back_button, user=user),
                    callback_data=CallbackData.section
                )
            ],
            [await main_menu_button(user)]
        ]
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


async def schedule_mode(user: User):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='По дням', callback_data=CallbackData.schedule_days)],
            [InlineKeyboardButton(text='По секциям', callback_data=CallbackData.schedule_sections)],
            [await main_menu_button(user)]
        ]
    )


async def schedule_dates(user: User):
    keyboard = []

    async for date in Schedule.objects.values_list('date', flat=True).order_by('date').distinct():
        if not date:
            continue

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=date.strftime('%d.%m.%Y'),
                    callback_data=f'schedule_date_{date.toordinal()}'
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text=await get_text(text_enum=TextEnum.back_button, user=user),
                callback_data=CallbackData.schedule
            )
        ]
    )
    keyboard.append([await main_menu_button(user)])
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


async def schedule_dates_list(user: User, date: datetime.date):
    keyboard = []

    async for s in Schedule.objects.filter(date=date):
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=s.ru_name if not user.lang else s.en_name,
                    callback_data=f'schedule_{s.id}'
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text=await get_text(text_enum=TextEnum.back_button, user=user),
                callback_data=CallbackData.schedule_days
            )
        ]
    )

    keyboard.append([await main_menu_button(user)])
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


async def schedule_sections(user: User):
    keyboard = []

    date: datetime.date
    async for sc in Schedule.objects.filter(section__isnull=False).distinct('section_id'):
        if not sc:
            continue

        s = await sync_to_async(lambda: sc.section)()
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=s.ru_name if not user.lang else s.en_name,
                    callback_data=f'schedule_section_{s.id}'
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text=await get_text(text_enum=TextEnum.back_button, user=user),
                callback_data=CallbackData.schedule
            )
        ]
    )

    keyboard.append([await main_menu_button(user)])
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


async def schedule_sections_list(user: User, se: Section):
    keyboard = []

    async for s in Schedule.objects.filter(section=se):
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=s.ru_name if not user.lang else s.en_name,
                    callback_data=f'schedule_{s.id}'
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text=await get_text(text_enum=TextEnum.back_button, user=user),
                callback_data=CallbackData.schedule_sections
            )
        ]
    )

    keyboard.append([await main_menu_button(user)])
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


async def schedule(user: User, s: Schedule):
    inline_keyboard = []

    if s.date:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text='В этот же день',
                    callback_data=f'schedule_date_{s.date.toordinal()}'
                )
            ]
        )

    se = await sync_to_async(lambda: s.section)()
    if se:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text='В этой же секции',
                    callback_data=f'schedule_section_{await sync_to_async(lambda: se.id)()}'
                )
            ]
        )

    inline_keyboard.append([await main_menu_button(user)])

    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
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
