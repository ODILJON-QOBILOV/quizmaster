# Generated by Django 5.1.3 on 2024-12-08 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_alter_shop_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='discount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]