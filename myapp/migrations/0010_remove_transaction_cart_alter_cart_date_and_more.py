# Generated by Django 4.2.6 on 2023-11-21 04:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_cart_date_transaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='cart',
        ),
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 21, 4, 16, 26, 220509, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 11, 21, 4, 16, 26, 221505, tzinfo=datetime.timezone.utc)),
        ),
    ]
