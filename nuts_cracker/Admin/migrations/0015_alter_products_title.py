# Generated by Django 5.1 on 2024-09-21 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0014_alter_products_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
