# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 09:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20170314_1450'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-pk',)},
        ),
    ]