# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-05-09 17:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yougam', '0004_auto_20190510_0147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='video',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='yougam.Video'),
        ),
    ]