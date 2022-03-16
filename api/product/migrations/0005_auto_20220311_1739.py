# Generated by Django 3.2 on 2022-03-11 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20220311_1438'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='buying_price',
        ),
        migrations.AddField(
            model_name='product',
            name='selling_price',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
    ]