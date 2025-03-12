from django.db import models

from accounts.models import User
from boards.models import TaskList


class Card(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name="cards")
    due_date = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.list.title} - {self.title}"

    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"


class Attachment(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="attachments")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()


class CardMember(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.card.title} - {self.user.email}"

    class Meta:
        unique_together = ('card', 'user')
        verbose_name = "CardMember"
        verbose_name_plural = "CardMembers"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    image = models.ImageField(upload_to="comment-images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.card.title} - comment by {self.user.email}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"