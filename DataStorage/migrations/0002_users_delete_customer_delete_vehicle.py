# Generated by Django 4.0.4 on 2022-08-31 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataStorage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('user_id', models.IntegerField(max_length=6, unique=True)),
                ('user_role', models.CharField(choices=[('Customer', 'Customer'), ('Admin', 'Admin')], max_length=10)),
                ('user_name', models.CharField(max_length=100)),
                ('contact', models.BigIntegerField(max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Vehicle',
        ),
    ]
