# Generated by Django 5.0.6 on 2024-08-01 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0006_alter_productreview_rating'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productreview',
            options={'ordering': ['-created_at'], 'verbose_name': 'نظر محصول', 'verbose_name_plural': 'نظرات محصول'},
        ),
    ]