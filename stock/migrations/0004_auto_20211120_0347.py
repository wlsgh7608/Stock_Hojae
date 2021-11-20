# Generated by Django 3.2.8 on 2021-11-19 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_rename_dae_newscontents_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='newscontents',
            name='summary',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
        migrations.AlterField(
            model_name='newscontents',
            name='translation',
            field=models.CharField(blank=True, default='', max_length=5000),
        ),
    ]
