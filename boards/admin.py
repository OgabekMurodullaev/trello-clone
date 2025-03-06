from django.contrib import admin
from .models import Board, TaskList


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'workspace', 'visibility')
    search_fields = ('title', 'workspace__name')
    list_filter = ('visibility',)


@admin.register(TaskList)
class ListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'board')
    search_fields = ('title', 'board__title')