# Generated by Django 3.2.8 on 2021-11-19 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_newscontents'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newscontents',
            old_name='dae',
            new_name='date',
        ),
    ]