# Generated by Django 4.0.4 on 2022-09-02 15:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataStorage', '0009_alter_booking_booking_date_passenger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 2, 20, 48, 52, 549776)),
        ),
    ]