# Generated by Django 4.0.6 on 2023-12-07 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_remove_order_invoice_shippingmethod_delivery_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status_ordered',
            field=models.BooleanField(default=False),
        ),
    ]
