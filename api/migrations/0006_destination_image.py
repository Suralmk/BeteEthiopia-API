# Generated by Django 4.1.11 on 2024-04-09 19:52

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_price_destination'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='image',
            field=models.ImageField(default='duck.png', upload_to=api.models.image_directory_path),
        ),
    ]
