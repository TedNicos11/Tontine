# Generated by Django 4.1.4 on 2023-01-04 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tontine',
            name='slug',
            field=models.SlugField(max_length=150, unique=True),
        ),
    ]
