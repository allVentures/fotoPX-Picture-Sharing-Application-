# Generated by Django 2.1.3 on 2018-11-26 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fotoPXapp', '0002_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
