# Generated by Django 4.1.4 on 2023-01-04 02:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_tontine_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tontine',
            name='slug',
        ),
    ]
