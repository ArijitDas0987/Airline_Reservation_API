# Generated by Django 4.0.4 on 2022-10-08 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataStorage', '0015_alter_booking_booking_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateTimeField(),
        ),
    ]