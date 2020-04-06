# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-12-19 06:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0005_auto_20191218_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='icon',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='图标'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='title',
            field=models.CharField(max_length=32, verbose_name='菜单名称'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='weight',
            field=models.IntegerField(default=100, verbose_name='权重'),
        ),
    ]
