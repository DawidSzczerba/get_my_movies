# Generated by Django 3.1.6 on 2021-02-08 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moviesweb', '0002_auto_20210208_2206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='user_rate',
        ),
    ]
