# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('symbol', models.CharField(unique=True, max_length=10)),
                ('fifty_moving_avg', models.FloatField()),
                ('two_hundred_moving_avg', models.FloatField()),
                ('year_high', models.FloatField()),
                ('year_low', models.FloatField()),
                ('price_change_pct', models.FloatField()),
                ('price_change_dol', models.FloatField()),
                ('twenty_four_hours_price_list', models.TextField()),
                ('last_ploted_at', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
