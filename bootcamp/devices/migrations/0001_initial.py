# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-22 08:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collaborator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('user',),
                'verbose_name': 'Collaborator',
                'verbose_name_plural': 'Collaborators',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('identification', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(max_length=4000)),
                ('location', models.CharField(choices=[('D', 'Draft'), ('P', 'Published')], default='D', max_length=1)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('create_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('update_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-create_date',),
                'verbose_name': 'Device',
                'verbose_name_plural': 'Devices',
            },
        ),
        migrations.CreateModel(
            name='DeviceComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=500)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.Device')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date',),
                'verbose_name': 'Device Comment',
                'verbose_name_plural': 'Device Comments',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=50)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.Device')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.AddField(
            model_name='collaborator',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.Device'),
        ),
        migrations.AddField(
            model_name='collaborator',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_collaborator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('tag', 'device')]),
        ),
        migrations.AlterIndexTogether(
            name='tag',
            index_together=set([('tag', 'device')]),
        ),
    ]