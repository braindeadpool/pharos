# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-07 04:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_material'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ('-create_date',), 'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
        migrations.AlterModelOptions(
            name='projectcomment',
            options={'ordering': ('date',), 'verbose_name': 'project Comment', 'verbose_name_plural': 'project Comments'},
        ),
    ]
