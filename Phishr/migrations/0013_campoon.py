# Generated by Django 2.0.5 on 2018-05-31 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Phishr', '0012_yeet_paign'),
    ]

    operations = [
        migrations.CreateModel(
            name='CAMPOON',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('company_id', models.CharField(max_length=100)),
                ('clicked_link', models.BooleanField(default=False)),
                ('employee_id', models.CharField(default='DEFAULT', max_length=20)),
            ],
        ),
    ]
