# Generated by Django 4.2.6 on 2023-11-23 04:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_transaction_cart_alter_cart_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='cart',
        ),
        migrations.AddField(
            model_name='transaction',
            name='prod',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='qty',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 23, 4, 12, 35, 135764, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 11, 23, 4, 12, 35, 136762, tzinfo=datetime.timezone.utc)),
        ),
    ]
