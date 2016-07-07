# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('councilmatic_core', '0011_bill_extras'),
        ('chicago', '0003_auto_20160623_1843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chicagobill',
            name='bill_ptr',
        ),
        migrations.DeleteModel(
            name='ChicagoBill',
        ),
        migrations.CreateModel(
            name='ChicagoBill',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('councilmatic_core.bill',),
        ),
    ]
