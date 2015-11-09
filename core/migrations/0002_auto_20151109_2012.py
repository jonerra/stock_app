# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='title',
            new_name='company',
        ),
        migrations.AddField(
            model_name='stock',
            name='symbol',
            field=models.CharField(default='test', max_length=300),
            preserve_default=False,
        ),
    ]
