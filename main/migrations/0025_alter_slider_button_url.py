# Generated by Django 4.0.6 on 2023-12-20 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_slider_main_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='button_url',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
