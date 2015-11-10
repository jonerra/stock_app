# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='review',
            field=models.ForeignKey(blank=True, to='core.Review', null=True),
        ),
        migrations.AlterField(
            model_name='vote',
            name='stock',
            field=models.ForeignKey(blank=True, to='core.Stock', null=True),
        ),
    ]
