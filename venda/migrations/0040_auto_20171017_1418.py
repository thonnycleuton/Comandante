# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-17 17:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venda', '0039_auto_20171017_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='data_pagamento',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 10, 17, 14, 18, 46, 586044)),
        ),
    ]