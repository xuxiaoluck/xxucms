# Generated by Django 2.1 on 2018-04-16 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_auto_20180412_1246'),
    ]

    operations = [
        migrations.CreateModel(
            name='stock_basics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=20)),
                ('industry', models.CharField(max_length=20)),
                ('area', models.CharField(max_length=20)),
                ('pe', models.FloatField()),
                ('outstanding', models.FloatField()),
                ('totals', models.FloatField()),
                ('totalAssets', models.FloatField()),
                ('liquidAssets', models.FloatField()),
                ('fixedAssets', models.FloatField()),
                ('reserved', models.FloatField()),
                ('reservedPerShare', models.FloatField()),
                ('esp', models.FloatField()),
                ('bvps', models.FloatField()),
                ('pb', models.FloatField()),
                ('timeToMarket', models.IntegerField()),
                ('undp', models.FloatField()),
                ('perundp', models.FloatField()),
                ('rev', models.FloatField()),
                ('profit', models.FloatField()),
                ('gpr', models.FloatField()),
                ('npr', models.FloatField()),
                ('holders', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='stock_cashflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=20)),
                ('cf_sales', models.FloatField()),
                ('rateofreturn', models.FloatField()),
                ('cf_nm', models.FloatField()),
                ('cf_liabilities', models.FloatField()),
                ('cashflowratio', models.FloatField()),
                ('report_date', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='stock_deptpaying',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=20)),
                ('currentratio', models.FloatField()),
                ('quickratio', models.FloatField()),
                ('cashratio', models.FloatField()),
                ('icratio', models.FloatField()),
                ('sheqratio', models.FloatField()),
                ('adratio', models.FloatField()),
                ('report_date', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='stock_growth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=20)),
                ('mbrg', models.FloatField()),
                ('nprg', models.FloatField()),
                ('nav', models.FloatField()),
                ('targ', models.FloatField()),
                ('epsg', models.FloatField()),
                ('seg', models.FloatField()),
                ('report_date', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='stock_operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=20)),
                ('arturnover', models.FloatField()),
                ('arturndays', models.FloatField()),
                ('inventory_turnover', models.FloatField()),
                ('inventory_days', models.FloatField()),
                ('currentasset_turnover', models.FloatField()),
                ('currentasset_days', models.FloatField()),
                ('report_date', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='stock_profit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=20)),
                ('roe', models.FloatField()),
                ('net_profit_ratio', models.FloatField()),
                ('gross_profit_rate', models.FloatField()),
                ('net_profits', models.FloatField()),
                ('esp', models.FloatField()),
                ('business_income', models.FloatField()),
                ('bips', models.FloatField()),
                ('report_date', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='stock_reports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=20)),
                ('esp', models.FloatField()),
                ('eps_yoy', models.FloatField()),
                ('roe', models.FloatField()),
                ('epcf', models.FloatField()),
                ('net_profits', models.FloatField()),
                ('profits_yoy', models.FloatField()),
                ('distrib', models.CharField(max_length=100)),
                ('report_date', models.CharField(max_length=6)),
            ],
        ),
    ]