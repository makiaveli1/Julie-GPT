# Generated by Django 4.2.6 on 2023-11-16 10:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chatbot", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="chat",
            name="assistant_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="chat",
            name="thread_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
