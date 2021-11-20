# Generated by Django 3.2.8 on 2021-11-19 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newscontents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dae', models.DateField()),
                ('title', models.CharField(max_length=256)),
                ('url', models.CharField(max_length=128)),
                ('content', models.CharField(max_length=5000)),
                ('translation', models.CharField(blank=True, default='', max_length=512)),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.usstocklist')),
            ],
        ),
    ]
