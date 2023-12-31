# Generated by Django 4.2.6 on 2023-10-15 07:58

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('links', '0004_alter_link_date_posted'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='posted_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='link',
            name='date_posted',
            field=models.DateField(default=datetime.datetime(2023, 10, 15, 7, 58, 47, 637714, tzinfo=datetime.timezone.utc)),
        ),
    ]
