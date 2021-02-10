# Generated by Django 3.1.6 on 2021-02-08 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moviesweb', '0004_auto_20210208_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='reviewed_movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='moviesweb.movie'),
        ),
    ]
