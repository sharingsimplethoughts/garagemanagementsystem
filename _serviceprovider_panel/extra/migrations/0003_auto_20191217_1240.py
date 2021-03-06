# Generated by Django 2.2.1 on 2019-12-17 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extra', '0002_auto_20191216_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutus',
            name='content_ar',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='title_ar',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='faq',
            name='content_ar',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='faq',
            name='title_ar',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='help',
            name='content_ar',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='help',
            name='title_ar',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='legal',
            name='content_ar',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='legal',
            name='title_ar',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='newoptions',
            name='content_ar',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='newoptions',
            name='title_ar',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='notification',
            name='description_ar',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='notification',
            name='title_ar',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AddField(
            model_name='privacypolicy',
            name='content_ar',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='privacypolicy',
            name='title_ar',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='termsandcondition',
            name='content_ar',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='termsandcondition',
            name='title_ar',
            field=models.CharField(default='', max_length=100),
        ),
    ]
