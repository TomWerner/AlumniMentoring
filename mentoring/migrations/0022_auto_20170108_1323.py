# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-08 19:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mentoring', '0021_auto_20161215_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('giver', models.CharField(choices=[('1', 'Mentor'), ('2', 'Mentee')], max_length=1)),
                ('went_well', models.TextField(max_length=1000)),
                ('went_poorly', models.TextField(max_length=1000)),
                ('other', models.TextField(max_length=1000)),
            ],
        ),
        migrations.RemoveField(
            model_name='mentormenteepairs',
            name='comments',
        ),
        migrations.AddField(
            model_name='feedback',
            name='pairing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentoring.MentorMenteePairs'),
        ),
    ]
