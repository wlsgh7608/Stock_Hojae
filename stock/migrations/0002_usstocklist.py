# Generated by Django 3.2.8 on 2021-10-06 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsStocklist',
            fields=[
                ('symbol', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('industry', models.CharField(max_length=50)),
                ('industry_id', models.IntegerField()),
                ('update_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'us_stocklist',
                'managed': False,
            },
        ),
    ]
