# Generated by Django 2.0 on 2018-01-14 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='作者')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='图书名称')),
                ('detial', models.TextField(verbose_name='内容简介')),
                ('uploadtime', models.DateTimeField(auto_now_add=True, verbose_name='上传时间')),
                ('uploaduser', models.CharField(max_length=30, verbose_name='上传用户')),
                ('accessnums', models.IntegerField(verbose_name='访问次数')),
                ('thumbupnums', models.IntegerField(verbose_name='点赞')),
                ('authors', models.ManyToManyField(to='ebook.Author')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='BookType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='分类名称')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='出版社名称')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='books',
            name='booktype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ebook.BookType'),
        ),
        migrations.AddField(
            model_name='books',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ebook.Publisher'),
        ),
    ]
