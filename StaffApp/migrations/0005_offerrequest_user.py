# Generated by Django 3.2.8 on 2021-11-09 17:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('StaffApp', '0004_alter_offerrequest_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerrequest',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offerrequest', to=settings.AUTH_USER_MODEL),
        ),
    ]
