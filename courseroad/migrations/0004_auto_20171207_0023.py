# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-07 00:23
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courseroad', '0003_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bucket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('custom', models.BooleanField(default=False)),
                ('type', models.CharField(max_length=10)),
                ('index', models.IntegerField()),
                ('requirement_obj', picklefield.fields.PickledObjectField(editable=False)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buckets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='semester',
            unique_together=set([('semester_id', 'year')]),
        ),
        migrations.AlterUniqueTogether(
            name='usersubject',
            unique_together=set([('subject', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='year',
            unique_together=set([('year_id', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='bucket',
            unique_together=set([('name', 'user'), ('index', 'user')]),
        ),
    ]
