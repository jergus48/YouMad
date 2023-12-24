# Generated by Django 4.0.6 on 2023-10-22 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_category_options_alter_products_options_size'),
    ]

    operations = [
        migrations.RenameField(
            model_name='size',
            old_name='size_name',
            new_name='size',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.order'),
        ),
    ]