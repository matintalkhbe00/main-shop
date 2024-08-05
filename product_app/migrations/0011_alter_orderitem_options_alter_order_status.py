# Generated by Django 5.0.6 on 2024-08-03 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0010_order_original_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'ایتم سفرش', 'verbose_name_plural': 'ایتم های سفارش'},
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('notRegistered', 'تایید نشده'), ('pending', 'در حال پردازش'), ('shipped', 'ارسال شده'), ('delivered', 'تحویل شده'), ('cancelled', 'لغو شده')], default='pending', max_length=20, verbose_name='وضعیت'),
        ),
    ]
