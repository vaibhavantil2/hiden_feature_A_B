# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-23 10:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_remove_ffadminuser_organisation'),
    ]

    operations = [
        migrations.AddField(
            model_name='invite',
            name='frontend_base_url',
            field=models.CharField(default='http://localhost:8000/invite', max_length=500),
            preserve_default=False,
        ),
    ]
