# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-16 04:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venda', '0069_auto_20171116_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='data_pagamento',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 11, 16, 1, 7, 25, 40180)),
        ),
    ]
