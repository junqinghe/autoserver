# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-15 14:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessunit',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.UserProfile'),
        ),
    ]
