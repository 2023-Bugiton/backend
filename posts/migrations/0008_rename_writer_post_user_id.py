# Generated by Django 4.2.2 on 2023-07-03 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_rename_user_id_post_writer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='writer',
            new_name='user_id',
        ),
    ]
