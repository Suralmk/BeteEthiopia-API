# Generated by Django 5.0.3 on 2024-04-06 19:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_destination_touragent_destinationimages_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.touragent')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.destination')),
            ],
        ),
    ]
