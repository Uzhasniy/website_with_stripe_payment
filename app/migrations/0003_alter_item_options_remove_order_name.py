# Generated by Django 4.1.1 on 2022-09-16 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_item_price_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={},
        ),
        migrations.RemoveField(
            model_name='order',
            name='name',
        ),
    ]
