# Generated by Django 3.2.3 on 2021-07-01 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='zoomed_img',
            field=models.ImageField(blank=True, null=True, upload_to='media/products/zoomed_img'),
        ),
    ]
