# Generated by Django 2.2.1 on 2019-12-17 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saccounts', '0002_auto_20191216_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiclemodle',
            name='model_name_ar',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='vehiclemodle',
            name='slug_ar',
            field=models.SlugField(default='', max_length=100),
        ),
    ]
