# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=120, verbose_name='subject')),
                ('body', models.TextField(verbose_name='body', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='visitor', blank=True)),
                ('sent_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='sent at')),
                ('read_at', models.DateTimeField(null=True, verbose_name='read at', blank=True)),
                ('replied_at', models.DateTimeField(null=True, verbose_name='replied at', blank=True)),
                ('sender_archived', models.BooleanField(default=False, verbose_name='archived by sender')),
                ('recipient_archived', models.BooleanField(default=False, verbose_name='archived by recipient')),
                ('sender_deleted_at', models.DateTimeField(null=True, verbose_name='deleted by sender at', blank=True)),
                ('recipient_deleted_at', models.DateTimeField(null=True, verbose_name='deleted by recipient at', blank=True)),
                ('moderation_status', models.CharField(default='p', max_length=1, verbose_name='status', choices=[('p', 'Pending'), ('a', 'Accepted'), ('r', 'Rejected')])),
                ('moderation_date', models.DateTimeField(null=True, verbose_name='moderated at', blank=True)),
                ('moderation_reason', models.CharField(max_length=120, verbose_name='rejection reason', blank=True)),
                ('moderation_by', models.ForeignKey(related_name='moderated_messages', verbose_name='moderator', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('parent', models.ForeignKey(related_name='next_messages', verbose_name='parent message', blank=True, to='postman.Message', null=True)),
                ('recipient', models.ForeignKey(related_name='received_messages', verbose_name='recipient', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('sender', models.ForeignKey(related_name='sent_messages', verbose_name='sender', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('thread', models.ForeignKey(related_name='child_messages', verbose_name='root message', blank=True, to='postman.Message', null=True)),
            ],
            options={
                'ordering': ['-sent_at', '-id'],
                'verbose_name': 'message',
                'verbose_name_plural': 'messages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PendingMessage',
            fields=[
            ],
            options={
                'verbose_name': 'pending message',
                'proxy': True,
                'verbose_name_plural': 'pending messages',
            },
            bases=('postman.message',),
        ),
    ]
