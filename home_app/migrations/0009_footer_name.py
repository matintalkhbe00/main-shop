# Generated by Django 5.0.6 on 2024-08-17 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_app', '0008_footer_id_eitaa_footer_id_instagram_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='footer',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='اسم شرکت'),
        ),
    ]