# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-16 23:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mentoring', '0003_auto_20161016_1818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menteeeducation',
            name='degree',
        ),
        migrations.RemoveField(
            model_name='menteeeducation',
            name='mentor',
        ),
        migrations.AddField(
            model_name='menteeeducation',
            name='mentee',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='mentoring.Mentee'),
            preserve_default=False,
        ),
    ]
