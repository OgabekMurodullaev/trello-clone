from django.contrib import admin
from .models import (
    Board, List, Card,
    CardMember, Label, CardLabel, Checklist, ChecklistItem, Comment, Attachment
)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'workspace', 'visibility')
    search_fields = ('title', 'workspace__name')
    list_filter = ('visibility',)


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('title', 'board')
    search_fields = ('title', 'board__title')


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('title', 'list', 'due_date')
    search_fields = ('title', 'list__title')
    list_filter = ('due_date',)


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('card', 'uploaded_by', 'uploaded_at')


@admin.register(CardMember)
class CardMemberAdmin(admin.ModelAdmin):
    list_display = ('card', 'user', 'added_at')
    search_fields = ('card__title', 'user__email')


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(CardLabel)
class CardLabelAdmin(admin.ModelAdmin):
    list_display = ('card', 'label')
    search_fields = ('card__title', 'label__title')


@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('title', 'card')
    search_fields = ('title', 'card__title')


@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('checklist', 'text', 'is_completed')
    search_fields = ('checklist__title', 'text')
    list_filter = ('is_completed',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'card', 'created_at')
    search_fields = ('user__email', 'card__title', 'text')
    list_filter = ('created_at', 'updated_at')
