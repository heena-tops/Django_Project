# Generated by Django 4.2.6 on 2023-11-21 03:43

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_user_image_alter_cart_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 21, 3, 43, 12, 503900, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grand_amount', models.IntegerField()),
                ('date', models.DateField(default=datetime.datetime(2023, 11, 21, 3, 43, 12, 504898, tzinfo=datetime.timezone.utc))),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.cart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
    ]
