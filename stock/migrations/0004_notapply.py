# Generated by Django 3.2.8 on 2021-10-17 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_delete_newday'),
    ]

    operations = [
        migrations.CreateModel(
            name='notapply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('anb', models.IntegerField()),
                ('pub_date', models.DateField()),
            ],
        ),
    ]
