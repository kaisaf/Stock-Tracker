# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock_scraper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('variation', models.FloatField()),
                ('minutes', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('variation_type', models.CharField(choices=[('PCT', 'Percent'), ('PR', 'Price'), ('VOL', 'Volume'), ('STD', 'Standard Deviation')], max_length=3)),
                ('symbol', models.ForeignKey(to='stock_scraper.Stock')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
