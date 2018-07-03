# Generated by Django 2.0.5 on 2018-05-17 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='target',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=13)),
                ('company_id', models.CharField(max_length=10)),
                ('company_name', models.CharField(max_length=100)),
                ('join_date', models.DateField()),
                ('TEMP_CAMPAIGN_RECORDS', models.CharField(max_length=200)),
            ],
        ),
    ]
