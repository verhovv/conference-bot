from django.db import models


class User(models.Model):
    id = models.BigIntegerField('Идентификатор Телеграм', primary_key=True, blank=False)

    username = models.CharField('Юзернейм', max_length=64, null=True, blank=True)
    first_name = models.CharField('Имя', null=True, blank=True)
    last_name = models.CharField('Фамилия', null=True, blank=True)

    created_at = models.DateTimeField('Дата регистрации', auto_now_add=True, blank=True)
    lang = models.BooleanField(default=False)

    def __str__(self):
        return f'id{self.id} | @{self.username or "-"} {self.first_name or "-"} {self.last_name or "-"}'

    class Meta:
        verbose_name = 'Телеграм пользователь'
        verbose_name_plural = 'Телеграм пользователи'


class JobTitle(models.Model):
    ru_name = models.CharField('Название Сферы/Должности на русском')
    en_name = models.CharField('Название Сферы/Должности на английском')

    class Meta:
        verbose_name = 'Сфера/Должность'
        verbose_name_plural = 'Сферы/Должности'

    def __str__(self):
        return self.ru_name


class Contact(models.Model):
    job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True, verbose_name='Сфера/Должность')
    ru_fio = models.CharField('ФИО на русском')
    en_fio = models.CharField('ФИО на английском')
    number = models.CharField('Номер телефона')
    link = models.CharField('Ссылка на соц сети')
    ru_description = models.TextField('Описание на русском')
    en_description = models.TextField('Описание на английском')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return self.ru_fio


class FAQ(models.Model):
    ru_question = models.CharField('Вопрос на русском')
    en_question = models.CharField('Вопрос на английском')
    ru_answer = models.TextField('Ответ на русском')
    en_answer = models.TextField('Ответ на английском')

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'

    def __str__(self):
        return self.ru_question


class Schedule(models.Model):
    ru_name = models.CharField('Название на русском')
    en_name = models.CharField('Название на английском')
    ru_description = models.TextField('Описание на русском')
    en_description = models.TextField('Описание на английском')

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'

    def __str__(self):
        return self.ru_name


class Section(models.Model):
    ru_name = models.CharField('Название на русском')
    en_name = models.CharField('Название на английском')
    ru_description = models.TextField('Описание на русском')
    en_description = models.TextField('Описание на английском')

    class Meta:
        verbose_name = 'Секция мероприятий'
        verbose_name_plural = 'Секции мероприятий'

    def __str__(self):
        return self.ru_name


class Activity(models.Model):
    ru_name = models.CharField('Название на русском')
    en_name = models.CharField('Название на английском')
    ru_description = models.TextField('Описание на русском')
    en_description = models.TextField('Описание на английском')

    class Meta:
        verbose_name = 'Активность мероприятий'
        verbose_name_plural = 'Активности мероприятий'

    def __str__(self):
        return self.ru_name


class Text(models.Model):
    types = {
        'photo': 'Фото',
        'video': 'Видео',
        'document': 'Документ'
    }
    name = models.CharField('Название текста', primary_key=True)
    ru_text = models.TextField('Текст на русском', null=True, blank=True)
    en_text = models.TextField('Текст на английском', null=True, blank=True)
    file_type = models.CharField('Тип файла', null=True, blank=True, choices=types)
    file = models.FileField('Файл', upload_to='web/media/files', null=True, blank=True)
    file_id = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            if self.pk:
                old_photo = Text.objects.get(pk=self.pk).file
                if old_photo != self.file:
                    self.file_id = None
        except:
            pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Текст'
        verbose_name_plural = 'Тексты'


class Attachments(models.Model):
    types = {
        'photo': 'Фото',
        'video': 'Видео',
        'document': 'Документ'
    }

    type = models.CharField('Тип вложения', choices=types)
    file = models.FileField('Файл', upload_to='web/media/mailing')
    file_id = models.TextField(null=True)
    mailing = models.ForeignKey('Mailing', on_delete=models.SET_NULL, null=True, related_name='attachments')

    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'


class Mailing(models.Model):
    text = models.TextField('Текст', blank=True, null=True)
    datetime = models.DateTimeField('Дата/Время')
    is_ok = models.BooleanField('Статус отправки', default=False)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
