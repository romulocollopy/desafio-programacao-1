# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('item_price', models.DecimalField(decimal_places=2, max_digits=14)),
                ('merchant_address', models.CharField(max_length=255)),
                ('purchase_count', models.PositiveSmallIntegerField()),
                ('item_description', models.TextField()),
                ('purchaser_name', models.CharField(max_length=255)),
                ('merchant_name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UploadAction',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='purchase',
            name='uploadaction',
            field=models.ForeignKey(to='core.UploadAction'),
            preserve_default=True,
        ),
    ]
