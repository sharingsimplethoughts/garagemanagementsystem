# Generated by Django 2.2.1 on 2019-12-19 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0003_auto_20191219_1306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptionplan',
            name='price_ar',
        ),
        migrations.RemoveField(
            model_name='subscriptionplan',
            name='valid_for_ar',
        ),
    ]
