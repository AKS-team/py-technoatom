# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-17 22:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20170517_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='roadmap',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.Roadmap', verbose_name='Дорожная карта'),
        ),
    ]
