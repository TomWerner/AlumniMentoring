# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-08-24 02:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mentoring', '0029_auto_20180823_2111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mentee',
            old_name='new_gender',
            new_name='gender',
        ),
        migrations.RenameField(
            model_name='mentor',
            old_name='new_gender',
            new_name='gender',
        ),
    ]
