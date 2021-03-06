# Generated by Django 2.1 on 2018-03-07 02:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('authors', models.CharField(max_length=20)),
                ('detial', models.TextField(verbose_name='内容简介')),
                ('accessnums', models.IntegerField(default=0)),
                ('thumbupnums', models.IntegerField(default=0, verbose_name='点赞')),
                ('updatetime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='BlogType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='blogs',
            name='blogtype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eblog.BlogType'),
        ),
    ]
