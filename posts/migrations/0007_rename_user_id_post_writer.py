# Generated by Django 4.2.2 on 2023-07-03 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_post_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user_id',
            new_name='writer',
        ),
    ]
