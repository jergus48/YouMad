# Generated by Django 4.0.6 on 2023-10-31 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_admininformations_alter_order_street'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admininformations',
            options={'verbose_name_plural': 'Admin Information'},
        ),
        migrations.AddField(
            model_name='admininformations',
            name='DPH',
            field=models.BooleanField(default=False),
        ),
    ]