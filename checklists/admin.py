from django.contrib import admin

from checklists.models import Checklist, ChecklistItem


@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('title', 'card')
    search_fields = ('title', 'card__title')


@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('checklist', 'text', 'is_completed')
    search_fields = ('checklist__title', 'text')
    list_filter = ('is_completed',)

