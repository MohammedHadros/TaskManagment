# Generated by Django 4.1.4 on 2023-08-25 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("task_app", "0004_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_email_varivied",
        ),
    ]
