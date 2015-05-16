# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import swampdragon.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('screen_name', models.CharField(max_length=50)),
                ('id_str', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(max_length=500, null=True)),
                ('hashtag', models.CharField(max_length=50, null=True)),
                ('tweet_id', models.CharField(max_length=50, null=True)),
            ],
            options={
            },
            bases=(swampdragon.models.SelfPublishModel, models.Model),
        ),
        migrations.CreateModel(
            name='TweetMention',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tweet', jsonfield.fields.JSONField()),
                ('id_str', models.CharField(max_length=50)),
                ('user_id_str', models.CharField(max_length=50)),
                ('retweeted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField()),
                ('account_id', models.ForeignKey(to='tweets.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TweetResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tweet', jsonfield.fields.JSONField()),
                ('id_str', models.CharField(max_length=50)),
                ('reply_id_str', models.CharField(max_length=50, null=True)),
                ('created_at', models.DateTimeField()),
                ('account_id', models.ForeignKey(to='tweets.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('screen_name', models.CharField(max_length=50, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
            ],
            options={
            },
            bases=(swampdragon.models.SelfPublishModel, models.Model),
        ),
        migrations.AddField(
            model_name='tweet',
            name='user_id',
            field=models.ForeignKey(to='tweets.User'),
            preserve_default=True,
        ),
    ]
