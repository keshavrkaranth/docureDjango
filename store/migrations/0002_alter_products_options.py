# Generated by Django 3.2.3 on 2021-05-23 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='products',
            options={'verbose_name': 'product', 'verbose_name_plural': 'products'},
        ),
    ]
