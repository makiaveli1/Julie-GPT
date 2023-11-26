# Generated by Django 4.2.6 on 2023-11-16 17:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chatbot", "0004_remove_chat_messages_chat_conversation_history"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chat",
            name="conversation_history",
        ),
        migrations.AddField(
            model_name="chat",
            name="messages",
            field=models.JSONField(default=dict),
        ),
    ]