# Generated by Django 2.0 on 2018-01-17 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ebook', '0002_books_uploadfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='名称')),
                ('uploadfile', models.FileField(upload_to='', verbose_name='文件')),
                ('uploadtime', models.DateTimeField(auto_now_add=True, verbose_name='上传时间')),
                ('uploaduser', models.CharField(max_length=30, verbose_name='上传用户')),
                ('accessnums', models.IntegerField(verbose_name='访问次数')),
                ('thumbupnums', models.IntegerField(verbose_name='点赞')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.RemoveField(
            model_name='books',
            name='accessnums',
        ),
        migrations.RemoveField(
            model_name='books',
            name='thumbupnums',
        ),
        migrations.RemoveField(
            model_name='books',
            name='uploadfile',
        ),
        migrations.RemoveField(
            model_name='books',
            name='uploadtime',
        ),
        migrations.RemoveField(
            model_name='books',
            name='uploaduser',
        ),
        migrations.AddField(
            model_name='bookfiles',
            name='book_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ebook.Books'),
        ),
    ]