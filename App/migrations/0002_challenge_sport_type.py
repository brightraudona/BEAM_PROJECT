# Generated by Django 4.1.7 on 2023-03-23 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='sport_type',
            field=models.TextField(default=''),
        ),
    ]
