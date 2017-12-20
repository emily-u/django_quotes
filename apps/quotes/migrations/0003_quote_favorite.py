# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-19 20:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0002_quote'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='favorite',
            field=models.ManyToManyField(related_name='Favorites', to='quotes.User'),
        ),
    ]