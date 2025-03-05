from django.db import models

from accounts.models import User
from workspaces.models import Workspace


class Board(models.Model):
    VISIBILITY_CHOICES = (
        ('private', 'Private'),
        ('public', 'Public'),
        ('workspace', 'Workspace')
    )

    title = models.CharField(max_length=120)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="boards")
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='private')
    background = models.ImageField(upload_to='board-backgrounds/', null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.workspace.name} - {self.title}"

    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"

class List(models.Model):
    title = models.CharField(max_length=120)
    colour = models.CharField(max_length=7, help_text="Hex color (e.g. #FF5733)")
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="lists")

    objects = models.Manager()

    def __str__(self):
        return f"{self.board.title} - {self.title}"

    class Meta:
        verbose_name = "List"
        verbose_name_plural = "Lists"

class Card(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="cards")
    due_date = models.DateTimeField(null=True, blank=True)

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


class CardMember(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card.title} - {self.user.email}"

    class Meta:
        unique_together = ('card', 'user')
        verbose_name = "CardMember"
        verbose_name_plural = "CardMembers"

class Label(models.Model):
    title = models.CharField(max_length=120)
    color = models.CharField(max_length=7, help_text="Hex color (e.g. #FF5733)")

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


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    image = models.ImageField(upload_to="comment-images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.card.title} - comment by {self.user.email}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"