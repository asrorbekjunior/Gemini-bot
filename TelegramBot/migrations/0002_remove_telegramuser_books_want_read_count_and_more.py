# Generated by Django 5.1.4 on 2024-12-30 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TelegramBot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegramuser',
            name='books_want_read_count',
        ),
        migrations.RemoveField(
            model_name='telegramuser',
            name='pages_count',
        ),
        migrations.RemoveField(
            model_name='telegramuser',
            name='read_books_name_count',
        ),
    ]
