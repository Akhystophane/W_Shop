# Generated by Django 4.1.4 on 2023-01-12 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_shopper_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopper',
            name='is_registered',
            field=models.BooleanField(default=False),
        ),
    ]
