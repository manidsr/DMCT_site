# Generated by Django 3.2.8 on 2021-12-04 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StaffApp', '0010_auto_20211115_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.IntegerField(),
        ),
    ]
