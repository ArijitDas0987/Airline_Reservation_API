# Generated by Django 4.0.4 on 2022-09-02 15:09

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DataStorage', '0008_alter_booking_booking_date_alter_booking_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 2, 20, 39, 42, 781259)),
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passenger_id', models.IntegerField(unique=True)),
                ('passenger_name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('booking_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataStorage.booking')),
            ],
        ),
    ]
