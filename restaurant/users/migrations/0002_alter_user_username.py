# Generated by Django 5.1.5 on 2025-02-09 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=64, verbose_name='نام کاربری'),
        ),
    ]
