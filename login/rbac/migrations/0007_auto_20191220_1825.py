# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-12-20 10:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0006_auto_20191219_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='roles',
        ),
        migrations.AlterField(
            model_name='permission',
            name='icon',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='图标'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Menu', verbose_name='一级菜单'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Permission', verbose_name='二级菜单'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='title',
            field=models.CharField(max_length=32, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='url',
            field=models.CharField(max_length=1200, verbose_name='url'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='url_name',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='url别名'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
