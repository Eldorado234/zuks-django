# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150308_2054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faq',
            name='question',
        ),
        migrations.AddField(
            model_name='faq',
            name='text',
            field=models.CharField(max_length=100, verbose_name='Text', unique=True, default=''),
            preserve_default=False,
        ),
    ]
