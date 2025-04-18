from django.contrib import admin

from checklists.models import CheckList, CheckListItem


@admin.register(CheckList)
class CheckListAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'card')
    search_fields = ('title', 'card__title')


@admin.register(CheckListItem)
class CheckListItemAdmin(admin.ModelAdmin):
    list_display = ('checklist', 'text', 'is_completed')
    search_fields = ('checklist__title', 'text')
    list_filter = ('is_completed',)

