from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

from bot.core import keyboards
from bot.core.keyboards import CallbackData
from bot.core.texts import TextEnum, get_text
from web.panel.models import User, JobTitle, Contact

router = Router()


@router.callback_query(F.data == CallbackData.contacts)
async def job_title(callback: CallbackQuery, user: User, bot: Bot):
    await callback.message.answer(
        text=await get_text(text_enum=TextEnum.job_title, user=user),
        reply_markup=await keyboards.job_title(user=user)
    )


@router.callback_query(F.data.startswith('job_'))
async def contact_list(callback: Message, user: User):
    *_, job_title_id = callback.data.split('_')
    job_title_id = int(job_title_id)

    job_title = await JobTitle.objects.aget(id=job_title_id)

    await callback.message.answer(
        text=job_title.ru_name if not user.lang else job_title.en_name,
        reply_markup=await keyboards.contacts(user=user, job_title_id=job_title_id)
    )


@router.callback_query(F.data.startswith('contact_'))
async def contact(callback: CallbackQuery, user: User, bot: Bot):
    *_, contact_id = callback.data.split('_')
    contact_id = int(contact_id)

    c = await Contact.objects.aget(id=contact_id)
    text = (
        f'{c.ru_fio if not user.lang else c.en_fio}\n'
        f'{c.number}\n'
        f'{c.link}\n'
        f'{c.ru_description if not user.lang else c.en_description}'
    )
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=await get_text(text_enum=TextEnum.back_button, user=user),
                    callback_data=f'job_{c.job_title_id}'
                )
            ],
            [await keyboards.main_menu_button(user=user)]
        ]
    )

    if not c.file:
        await callback.message.answer(
            text=text,
            reply_markup=reply_markup
        )
        return

    msg = await callback.message.answer_photo(
        photo=FSInputFile(path=c.file.path) if not c.file_id else c.file_id,
        caption=text,
        reply_markup=reply_markup
    )

    if not c.file_id:
        c.file_id = msg.photo[-1].file_id
        await c.asave()
