# Generated by Django 2.2.11 on 2021-09-28 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkinglot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spot',
            name='is_Occupied',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
