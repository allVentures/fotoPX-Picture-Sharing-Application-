# Generated by Django 2.1.3 on 2018-12-11 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fotoPXapp', '0018_auto_20181211_1845'),
    ]

    operations = [
        migrations.RenameField(
            model_name='picture',
            old_name='camera_producer',
            new_name='camera_model',
        ),
    ]
