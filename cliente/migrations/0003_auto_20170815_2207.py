# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-16 01:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0002_auto_20170814_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cod_cliente',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='cpf',
            field=models.CharField(blank=True, max_length=14),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
