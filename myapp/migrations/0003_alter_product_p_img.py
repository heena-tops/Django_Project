# Generated by Django 4.2.5 on 2023-10-05 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_product_p_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='p_img',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
