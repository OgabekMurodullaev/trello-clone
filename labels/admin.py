from django.contrib import admin

from labels.models import Label, CardLabel


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(CardLabel)
class CardLabelAdmin(admin.ModelAdmin):
    list_display = ('card', 'label')
    search_fields = ('card__title', 'label__title')


