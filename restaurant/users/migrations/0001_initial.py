# Generated by Django 5.1.5 on 2025-02-09 08:06

import utils
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64, unique=True, verbose_name='نام کاربری')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, validators=[utils.phone_validator], verbose_name='تلفن همراه')),
                ('password', models.CharField(blank=True, max_length=128, null=True, verbose_name='پسورد')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='ایجاد شده در')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='بروز شده در')),
                ('suspended_at', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ تعلیق')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
                'ordering': ['-id'],
            },
        ),
    ]
