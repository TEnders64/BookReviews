# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 00:59
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='book',
            managers=[
                ('bookMgr', django.db.models.manager.Manager()),
            ],
        ),
    ]