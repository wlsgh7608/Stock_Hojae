# Generated by Django 3.2.8 on 2021-11-22 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='portfolioname',
            options={'ordering': ['-share_date']},
        ),
        migrations.AddField(
            model_name='portfolioname',
            name='share_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
