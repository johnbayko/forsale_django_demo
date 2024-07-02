# Generated by Django 5.0.6 on 2024-07-01 20:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forsale', '0003_userinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='forsale.userinfo'),
            preserve_default=False,
        ),
    ]