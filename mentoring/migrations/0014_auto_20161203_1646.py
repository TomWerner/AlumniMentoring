# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-03 22:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentoring', '0013_auto_20161203_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menteecontactinformation',
            name='secondary_phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
