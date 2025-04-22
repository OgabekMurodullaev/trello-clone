import threading

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from activity_log.models import ActivityLog
from boards.models import TaskList
from cards.models import Card, Comment, Attachment, CardMember
from checklists.models import CheckListItem

_thread_locals = threading.local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)

# Card signals
@receiver(post_save, sender=Card)
def log_card_creation(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            board=instance.list.board,
            user=get_current_user(),
            action_type=ActivityLog.ActionType.CREATED,
            action_description=f"'{instance.title}' kartasi yaratildi."
        )

@receiver(post_delete, sender=Card)
def log_card_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        board=instance.list.board,
        user=get_current_user(),
        action_type=ActivityLog.ActionType.DELETED,
        action_description=f"'{instance.title}' kartasi o'chirildi."
    )

@receiver(pre_save, sender=Card)
def log_card_update(sender, instance, **kwargs):
    if instance.id:
        old_instance = Card.objects.get(id=instance.id)
        if old_instance.list_id != instance.list_id:
            old_list = old_instance.list
            new_list = instance.list
            ActivityLog.objects.create(
                board=instance.list.board,
                user=get_current_user(),
                action_type=ActivityLog.ActionType.MOVED,
                action_description=f"'{instance.title}' kartasi {old_list.title} ro'yxatidan {new_list.title} ro'yxatigaiga ko'chirildi."
            )
        elif old_instance.title != instance.title:
            ActivityLog.objects.create(
                board=instance.list.board,
                user=get_current_user(),
                action_type=ActivityLog.ActionType.UPDATED,
                action_description=f"'{old_instance.title}' karta sarlavhasi '{instance.title}' ga o'zgartirildi."
            )

# Comment signals
@receiver(post_save, sender=Comment)
def log_comment_creation(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            board=instance.card.list.board,
            user=get_current_user(),
            action_type=ActivityLog.ActionType.COMMENTED,
            action_description=f"'{instance.card.title}' kartasiga sharh qo‘shildi: '{instance.text[:50]}...'"
        )

# CheckListItem signals
@receiver(pre_save, sender=CheckListItem)
def log_checklist_item_update(sender, instance, **kwargs):
    if instance.id:
        old_instance = CheckListItem.objects.get(id=instance.id)
        if old_instance.status != instance.status:
            status = "bajarildi" if instance.is_completed else "bajarilmadi"
            ActivityLog.objects.create(
                board=instance.checklist.card.list.board,
                user=get_current_user(),
                action_type=ActivityLog.ActionType.COMPLETED,
                action_description=f"'{instance.checklist.card.title}' kartasidagi '{instance.text}' checklist elementi {status}."
            )

# TaskList signals
@receiver(post_save, sender=TaskList)
def log_tasklist_creation(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            board=instance.board,
            user=get_current_user(),
            action_type=ActivityLog.ActionType.CREATED,
            action_description=f"'{instance.title}' ro‘yxati yaratildi."
        )

@receiver(post_delete, sender=TaskList)
def log_tasklist_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        board=instance.board,
        user=get_current_user(),
        action_type=ActivityLog.ActionType.DELETED,
        action_description=f"'{instance.title}' ro‘yxati o‘chirildi."
    )

# Attachment signals
@receiver(post_save, sender=Attachment)
def log_attachment_created(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            board=instance.card.list.board,
            user=get_current_user(),
            action_type=ActivityLog.ActionType.OTHER,
            action_description=f"'{instance.card.title}' kartasiga fayl qo'shildi."
        )

# CardMember signals
@receiver(post_save, sender=CardMember)
def log_cardmember_creation(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            board=instance.card.list.board,
            user=get_current_user(),
            action_type=ActivityLog.ActionType.OTHER,
            action_description=f"'{instance.card.title}' kartasiga '{instance.user.email}' a’zo sifatida qo‘shildi."
        )

@receiver(post_delete, sender=CardMember)
def log_cardmember_deleted(sender, instance, **kwargs):
    ActivityLog.objects.create(
        board=instance.card.list.board,
        user=get_current_user(),
        action_type=ActivityLog.ActionType.OTHER,
        action_description=f"'{instance.card.title}' kartasidan '{instance.user.email}' a’zo sifatida o‘chirildi."
    )