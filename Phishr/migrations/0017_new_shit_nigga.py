# Generated by Django 2.0.5 on 2018-06-04 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Phishr', '0016_auto_20180604_1831'),
    ]

    operations = [
        migrations.CreateModel(
            name='NEW_SHIT_NIGGA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('company_id', models.CharField(max_length=100)),
                ('clicked_link', models.BooleanField(default=False)),
                ('employee_id', models.CharField(default='DEFAULT', max_length=64)),
            ],
        ),
    ]