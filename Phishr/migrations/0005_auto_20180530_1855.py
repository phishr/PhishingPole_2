# Generated by Django 2.0.5 on 2018-05-30 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Phishr', '0004_auto_20180530_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='ass_master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('company_id', models.CharField(max_length=100)),
                ('clicked_link', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='operation_test_1',
            name='description',
        ),
        migrations.RemoveField(
            model_name='operation_test_2',
            name='description',
        ),
        migrations.RemoveField(
            model_name='operation_test_3',
            name='description',
        ),
        migrations.RemoveField(
            model_name='operation_test_4',
            name='description',
        ),
        migrations.RemoveField(
            model_name='operation_test_5',
            name='description',
        ),
        migrations.RemoveField(
            model_name='operation_test_6',
            name='description',
        ),
        migrations.AddField(
            model_name='campaign_directory',
            name='description',
            field=models.CharField(default='N/A', max_length=200),
        ),
    ]
