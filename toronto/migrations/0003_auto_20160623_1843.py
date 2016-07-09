# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('councilmatic_core', '0010_auto_20160120_1248'),
        ('chicago', '0002_chicagoevent_torontoperson'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ChicagoBill',
        ),
        migrations.CreateModel(
            name='ChicagoBill',
            fields=[
                ('bill_ptr', models.OneToOneField(primary_key=True, auto_created=True, serialize=False, parent_link=True, to='councilmatic_core.Bill')),
                ('wards', jsonfield.fields.JSONField()),
            ],
            bases=('councilmatic_core.bill',),
        ),
    ]
