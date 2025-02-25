# Generated by Django 5.1.6 on 2025-02-20 16:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('workspaces', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('due_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Card',
                'verbose_name_plural': 'Cards',
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('color', models.CharField(help_text='Hex color (e.g. #FF5733)', max_length=7)),
            ],
            options={
                'verbose_name': 'Label',
                'verbose_name_plural': 'Labels',
            },
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('visibility', models.CharField(choices=[('private', 'Private'), ('public', 'Public'), ('workspace', 'Workspace')], default='private', max_length=10)),
                ('background', models.ImageField(blank=True, null=True, upload_to='board-backgrounds/')),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boards', to='workspaces.workspace')),
            ],
            options={
                'verbose_name': 'Board',
                'verbose_name_plural': 'Boards',
            },
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='attachments/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to=settings.AUTH_USER_MODEL)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='boards.card')),
            ],
        ),
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checklists', to='boards.card')),
            ],
            options={
                'verbose_name': 'Checklist',
                'verbose_name_plural': 'Checklists',
            },
        ),
        migrations.CreateModel(
            name='ChecklistItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('is_completed', models.BooleanField(default=False)),
                ('checklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='boards.checklist')),
            ],
            options={
                'verbose_name': 'ChecklistItem',
                'verbose_name_plural': 'ChecklistItems',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='comment-images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='boards.card')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='CardLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='labels', to='boards.card')),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='boards.label')),
            ],
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('colour', models.CharField(help_text='Hex color (e.g. #FF5733)', max_length=7)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lists', to='boards.board')),
            ],
            options={
                'verbose_name': 'List',
                'verbose_name_plural': 'Lists',
            },
        ),
        migrations.AddField(
            model_name='card',
            name='list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='boards.list'),
        ),
        migrations.CreateModel(
            name='CardMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='boards.card')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'CardMember',
                'verbose_name_plural': 'CardMembers',
                'unique_together': {('card', 'user')},
            },
        ),
    ]
