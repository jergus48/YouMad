# Generated by Django 4.0.6 on 2023-12-20 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_alter_slide_options_remove_products_category_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='products',
            options={},
        ),
        migrations.AlterModelOptions(
            name='slide',
            options={},
        ),
        migrations.AddField(
            model_name='slider',
            name='announcement_bar',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
