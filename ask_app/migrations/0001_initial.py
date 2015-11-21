# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import ask_app.models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('rating', models.IntegerField(default=0, db_index=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('isBestAnswer', models.BooleanField(default=False, db_index=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['rating'],
            },
        ),
        migrations.CreateModel(
            name='AnswerVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isDislike', models.BooleanField(default=b'False')),
                ('answer', models.ForeignKey(to='ask_app.Answer')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExtendedAskUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(unique=True, max_length=30)),
                ('userpic', models.FileField(upload_to=ask_app.models.userpic_upload_path, blank=True)),
                ('rating', models.IntegerField(default=0, db_index=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['rating'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('rating', models.IntegerField(default=0, db_index=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('answers_amount', models.PositiveIntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='QuestionVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isDislike', models.BooleanField(default=b'False')),
                ('question', models.ForeignKey(to='ask_app.Question')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tagName', models.CharField(unique=True, max_length=255)),
                ('rating', models.IntegerField(default=0, db_index=True)),
            ],
            options={
                'ordering': ['rating'],
            },
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='ask_app.Tag'),
        ),
        migrations.AddField(
            model_name='question',
            name='votes',
            field=models.ManyToManyField(related_query_name=b'QuestionVote', related_name='QuestionVotes', through='ask_app.QuestionVote', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='ask_app.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='votes',
            field=models.ManyToManyField(related_query_name=b'AnswerVote', related_name='AnswerVotes', through='ask_app.AnswerVote', to=settings.AUTH_USER_MODEL),
        ),
    ]
