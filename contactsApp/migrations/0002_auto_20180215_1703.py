# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-02-15 11:03
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactsApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(b'^\\+?1?\\d{9,15}$', b'Invalid phone number')]),
        ),
    ]
