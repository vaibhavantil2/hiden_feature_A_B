# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-09-06 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segments', '0006_auto_20190828_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condition',
            name='operator',
            field=models.CharField(choices=[('EQUAL', 'Exactly Matches'), ('GREATER_THAN', 'Greater than'), ('LESS_THAN', 'Less than'), ('CONTAINS', 'Contains'), ('GREATER_THAN_INCLUSIVE', 'Greater than or equal to'), ('LESS_THAN_INCLUSIVE', 'Less than or equal to'), ('NOT_CONTAINS', 'Does not contain'), ('NOT_EQUAL', 'Does not match'), ('REGEX', 'Matches regex'), ('PERCENTAGE_SPLIT', 'Percentage split')], max_length=500),
        ),
        migrations.AlterField(
            model_name='condition',
            name='property',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='segmentrule',
            name='type',
            field=models.CharField(choices=[('ALL', 'all'), ('ANY', 'any'), ('NONE', 'none')], max_length=50),
        ),
    ]
