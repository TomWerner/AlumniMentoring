# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-12-12 04:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentoring', '0024_remove_mentor_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentee',
            name='gender',
            field=models.CharField(choices=[('a', 'Agender'), ('c', 'Cisgender'), ('m', 'Male'), ('n', 'Non-binary'), ('t', 'Transgender'), ('f', 'Female'), ('l', 'Another gender not listed'), ('p', 'Prefer not to answer')], max_length=1),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='gender',
            field=models.CharField(choices=[('a', 'Agender'), ('c', 'Cisgender'), ('m', 'Male'), ('n', 'Non-binary'), ('t', 'Transgender'), ('f', 'Female'), ('l', 'Another gender not listed'), ('p', 'Prefer not to answer')], max_length=1),
        ),
        migrations.AlterField(
            model_name='mentoreducation',
            name='degree',
            field=models.CharField(choices=[('ba', 'Bachelor of Arts'), ('bs', 'Bachelor of Sciences'), ('m', 'Masters'), ('d', 'Ph.D'), ('pd', 'MD Ph.D'), ('md', 'MD'), ('jd', 'JD'), ('mp', 'MPhil')], max_length=3),
        ),
    ]