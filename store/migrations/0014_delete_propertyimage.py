# Generated by Django 4.1.4 on 2023-02-28 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_propertyimage_remove_product_album_delete_image_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PropertyImage',
        ),
    ]
