# Generated by Django 4.0.4 on 2022-09-02 12:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataStorage', '0006_rename_user_id_booking_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 2, 18, 11, 47, 395973)),
        ),
    ]
