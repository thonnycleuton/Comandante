# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-03 23:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venda', '0006_auto_20170903_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='tipo',
            field=models.IntegerField(choices=[(1, 'A vista'), (2, 'Prazo')], default=1),
        ),
    ]