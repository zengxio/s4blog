# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-02-27 03:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.ImageField(upload_to='static/imgs', verbose_name='头像'),
        ),
    ]
