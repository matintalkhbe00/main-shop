# Generated by Django 5.0.6 on 2024-08-07 14:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0015_category_subcategory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_at'], 'verbose_name': 'محصول', 'verbose_name_plural': 'محصولات'},
        ),
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ ایجاد'),
        ),
    ]