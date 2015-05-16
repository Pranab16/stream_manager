# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweetmention',
            name='tweet',
        ),
        migrations.RemoveField(
            model_name='tweetresponse',
            name='tweet',
        ),
    ]
