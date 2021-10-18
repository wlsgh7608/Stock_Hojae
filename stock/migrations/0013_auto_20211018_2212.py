# Generated by Django 3.2.8 on 2021-10-18 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0012_rename_total_assets_balancesheet_total_assets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balancesheet',
            name='total_assets',
            field=models.BigIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='total_current_assets',
            field=models.BigIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='total_current_liability',
            field=models.BigIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='total_liability',
            field=models.BigIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='total_stockholder_equity',
            field=models.BigIntegerField(default=0, null=True),
        ),
    ]