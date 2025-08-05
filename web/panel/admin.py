from django.contrib import admin
from web.panel.models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'created_at')
    fields = ('id', 'username', 'first_name', 'last_name', 'created_at')

    exclude = ('data',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class AttachmentsInline(admin.TabularInline):
    model = Attachments

    exclude = ('file_id',)

    extra = 0


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'text', 'is_ok']
    readonly_fields = ['is_ok']
    inlines = [AttachmentsInline]


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    exclude = ('file_id',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    pass


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    pass


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ('name', 'ru_text', 'en_text')
    fields = ('name', 'ru_text', 'en_text', 'file_type', 'file')
    readonly_fields = ('name',)

    def has_delete_permission(self, request, obj=...):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    exclude = ('file_id',)
