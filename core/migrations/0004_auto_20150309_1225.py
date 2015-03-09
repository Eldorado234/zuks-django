# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150308_2150'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faq',
            options={'verbose_name_plural': 'FAQ Questions', 'verbose_name': 'FAQ Question', 'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='faq',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True, default=0),
            preserve_default=False,
        ),
    ]
