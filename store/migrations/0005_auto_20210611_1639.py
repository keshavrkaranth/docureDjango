# Generated by Django 3.2.3 on 2021-06-11 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20210611_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='facts_img',
            field=models.ImageField(blank=True, null=True, upload_to='media/products/desc'),
        ),
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/products'),
        ),
    ]