# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-18 06:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venda', '0080_auto_20171117_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='data_pagamento',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 11, 18, 3, 58, 23, 932838)),
        ),
    ]
