# Generated by Django 4.2.6 on 2023-11-16 14:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chatbot", "0002_chat_assistant_id_chat_thread_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chat",
            name="message",
        ),
        migrations.RemoveField(
            model_name="chat",
            name="response",
        ),
        migrations.RemoveField(
            model_name="chat",
            name="timestamp",
        ),
        migrations.AddField(
            model_name="chat",
            name="last_updated",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="chat",
            name="messages",
            field=models.JSONField(default=dict),
        ),
    ]
