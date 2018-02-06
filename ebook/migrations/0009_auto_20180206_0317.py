# Generated by Django 2.0 on 2018-02-06 03:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ebook', '0008_auto_20180124_0215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookfiles',
            name='thumbupnums',
        ),
        migrations.RemoveField(
            model_name='bookfiles',
            name='uploadtime',
        ),
        migrations.RemoveField(
            model_name='bookfiles',
            name='uploaduser',
        ),
        migrations.AddField(
            model_name='books',
            name='accessnums',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='books',
            name='thumbupnums',
            field=models.IntegerField(default=0, verbose_name='点赞'),
        ),
        migrations.AddField(
            model_name='books',
            name='updatetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='上传时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='books',
            name='updateuser',
            field=models.CharField(default='defaultuser', max_length=30, verbose_name='uploaduser'),
        ),
    ]
