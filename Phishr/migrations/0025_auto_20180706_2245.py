# Generated by Django 2.0.5 on 2018-07-06 20:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Phishr', '0024_remove_campaign_results_campaign_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(default='NOT-SET', max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='CAMPOON',
        ),
        migrations.DeleteModel(
            name='companyco_trial_campaign',
        ),
        migrations.DeleteModel(
            name='FUCKME',
        ),
        migrations.DeleteModel(
            name='KIKE_ME',
        ),
        migrations.DeleteModel(
            name='new_campaign',
        ),
        migrations.DeleteModel(
            name='NEW_SHIT_NIGGA',
        ),
        migrations.DeleteModel(
            name='OPERATION_EAT_ASS',
        ),
        migrations.DeleteModel(
            name='operation_test_1',
        ),
        migrations.DeleteModel(
            name='operation_test_2',
        ),
        migrations.DeleteModel(
            name='operation_test_3',
        ),
        migrations.DeleteModel(
            name='operation_test_4',
        ),
        migrations.DeleteModel(
            name='operation_test_5',
        ),
        migrations.DeleteModel(
            name='operation_test_6',
        ),
        migrations.DeleteModel(
            name='Test_Icles',
        ),
        migrations.DeleteModel(
            name='YEET_PAIGN',
        ),
    ]
