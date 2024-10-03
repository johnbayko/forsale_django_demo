# Generated by Django 5.0.6 on 2024-08-20 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forsale', '0008_remove_items_sold_offers_accepted_unique'),
    ]

    operations = [
        migrations.AddField(
            model_name='offers',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddConstraint(
            model_name='offers',
            constraint=models.CheckConstraint(check=models.Q(('delivered', models.F('accepted')), ('delivered', False), _connector='OR'), name='delivered_accepted'),
        ),
    ]
