# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-12-18 05:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0004_permission_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='url_name',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='title',
            field=models.CharField(max_length=32, verbose_name='一级菜单'),
        ),
    ]
