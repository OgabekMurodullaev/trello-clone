from django.contrib import admin
from .models import *

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'list', 'due_date')
    search_fields = ('title', 'list__title')
    list_filter = ('due_date',)


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'card', 'uploaded_by', 'uploaded_at')


@admin.register(CardMember)
class CardMemberAdmin(admin.ModelAdmin):
    list_display = ('card', 'user', 'added_at')
    search_fields = ('card__title', 'user__email')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'card', 'created_at')
    search_fields = ('user__email', 'card__title', 'text')
    list_filter = ('created_at', 'updated_at')
