from django.db import models

from cards.models import Card


class Checklist(models.Model):
    title = models.CharField(max_length=120)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="checklists")

    def __str__(self):
        return f"{self.card.title} - {self.title}"

    class Meta:
        verbose_name = "Checklist"
        verbose_name_plural = "Checklists"


class ChecklistItem(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name="items")
    text = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.checklist.title} - {self.text[:50]}"

    class Meta:
        verbose_name = "ChecklistItem"
        verbose_name_plural = "ChecklistItems"
