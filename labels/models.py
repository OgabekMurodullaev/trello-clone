from django.db import models

from cards.models import Card


class Label(models.Model):
    title = models.CharField(max_length=120)
    color = models.CharField(max_length=7, help_text="Hex color (e.g. #FF5733)", default="#FFFFFF")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Label"
        verbose_name_plural = "Labels"

class CardLabel(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="labels")
    label = models.ForeignKey(Label, on_delete=models.CASCADE, related_name="cards")

    def __str__(self):
        return f"{self.card.title} - {self.label.title}"

