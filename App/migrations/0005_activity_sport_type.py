# Generated by Django 4.1.7 on 2023-03-24 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_alter_challenge_sport_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='sport_type',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]