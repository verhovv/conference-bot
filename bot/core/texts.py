from enum import StrEnum, auto
from web.panel.models import Text, User


class TextEnum(StrEnum):
    main_menu = 'Текст Главное меню'
    main_menu_button = 'Кнопка В главное меню'
    back_button = 'кнопка Назад'
    information = 'Информация о мероприятии'
    information_button = 'кнопка Информация о мероприятии'
    contact_button = 'кнопка Контакты'
    job_title = 'Текст к Сферам/Должностям'
    contact_job_title = 'Текст к разделам по контактам'
    schedule = 'Текст к расписанию'
    schedule_button = 'кнопка Расписание'
    map = 'Карта'
    map_button = 'Карта'
    section = 'Текст к секциям'
    section_button = 'кнопка Секции'
    memo = 'Памятка участников'
    memo_button = 'кнопка Памятка'
    chat_link = 'Ссылка на чат по секциям'
    phone_number = 'Номер телефона'
    phone_button = 'Кнопка ТГ аккаунт'
    tg_link = 'Ссылка на тг аккаунт'
    tg_channel_button = 'кнопка Канал'
    tg_channel_link = 'Ссылка на тг группу'
    faq_button = 'кнопка FAQ'
    faq = 'текст FAQ'
    support_button = 'кнопка Поддержка'
    lang_button = 'кнопка Смены языка'
    chat_button = 'кнопка Чат по секциям'
    map_in_button = 'кнопка внутри карт'
    map_in_button_link = 'ссылка на кнопку внутри карт',
    section_leading_button = 'кнопка Ведущие секции'
    section_schedule_button = 'кнопка Расписание секции',


default_texts = {
    TextEnum.main_menu: 'Главное меню',
    TextEnum.main_menu_button: 'В меню',
    TextEnum.back_button: 'Назад',
    TextEnum.information: 'Информация о мероприятии',
    TextEnum.information_button: 'Информация',
    TextEnum.contact_button: 'Контакты',
    TextEnum.job_title: 'Текст к Сферам/Должностям',
    TextEnum.contact_job_title: 'Текст к разделам по контактам',
    TextEnum.schedule: 'Текст к расписаниям',
    TextEnum.schedule_button: 'Расписание',
    TextEnum.map: 'Карта',
    TextEnum.map_button: 'кнопка Карта',
    TextEnum.section: 'Текст к секциям',
    TextEnum.section_button: 'Секции',
    TextEnum.memo: 'Информация',
    TextEnum.memo_button: 'Памятка участников',
    TextEnum.chat_link: 'https://t.me/verhovv',
    TextEnum.phone_number: '+7 (984) 153 97-68',
    TextEnum.phone_button: 'Телеграм аккаунт',
    TextEnum.tg_link: 'https://t.me/verhovv',
    TextEnum.tg_channel_button: 'Канал',
    TextEnum.tg_channel_link: 'https://t.me/verhovv',
    TextEnum.support_button: 'Поддержка',
    TextEnum.lang_button: 'RU',
    TextEnum.faq_button: 'FAQ',
    TextEnum.faq: 'FAQ',
    TextEnum.chat_button: 'Чат по секциям',
    TextEnum.map_in_button: 'План здания',
    TextEnum.map_in_button_link: 'https://t.me/verhovv.ru',
    TextEnum.section_leading_button: 'Ведущие',
    TextEnum.section_schedule_button: 'Расписание'
}


async def setup_texts():
    for text_enum in TextEnum:
        text, created = await Text.objects.aget_or_create(name=text_enum)
        if created:
            text.ru_text = default_texts[text_enum]
            await text.asave()


async def get_text(text_enum: TextEnum, user: User) -> str:
    text_instance = await Text.objects.aget(name=text_enum)
    return [text_instance.ru_text, text_instance.en_text][user.lang]
