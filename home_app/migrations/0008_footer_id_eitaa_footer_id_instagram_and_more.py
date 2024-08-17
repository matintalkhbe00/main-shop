# Generated by Django 5.0.6 on 2024-08-17 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_app', '0007_alter_footer_eitaa_alter_footer_instagram_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='footer',
            name='id_eitaa',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='آیدی ایتا شرکت'),
        ),
        migrations.AddField(
            model_name='footer',
            name='id_instagram',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='آیدی اینستاگرام شرکت'),
        ),
        migrations.AddField(
            model_name='footer',
            name='id_telegram',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='آیدی تلگرام شرکت'),
        ),
        migrations.AddField(
            model_name='footer',
            name='id_twitter',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='آیدی توییتر شرکت'),
        ),
    ]