# Generated by Django 2.1.3 on 2018-12-11 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fotoPXapp', '0017_auto_20181206_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='camera_producer',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='picture',
            name='creation_date',
            field=models.DateTimeField(null=True),
        ),
    ]