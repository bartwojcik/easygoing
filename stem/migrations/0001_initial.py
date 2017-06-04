# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-04 20:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('author_name', models.CharField(max_length=255, verbose_name='Nick')),
                ('author_email', models.EmailField(blank=True, max_length=254, verbose_name='E-mail')),
                ('content', models.TextField(verbose_name='Comment text')),
                ('taken_down', models.BooleanField(verbose_name='Hidden')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(verbose_name='Created')),
                ('edited', models.DateTimeField(null=True, verbose_name='Edited')),
                ('language', models.CharField(choices=[('en', 'English'), ('pl', 'Polski')], max_length=2, verbose_name='Language')),
                ('title', models.CharField(max_length=1024, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('content_processed', models.TextField()),
                ('blog_post', models.BooleanField(verbose_name='Is a blog post')),
                ('hidden', models.BooleanField(verbose_name='Is hidden')),
                ('comments_closed', models.BooleanField(verbose_name='Has closed comments')),
                ('number_of_comments', models.IntegerField(verbose_name='Number of comments')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default="Don't forget to edit me!", max_length=1024, verbose_name='Title')),
                ('header', models.TextField(blank=True, default="#Don't forget to edit me!#", verbose_name='Header')),
                ('header_processed', models.TextField()),
                ('sidebar', models.TextField(blank=True, default="##Don't forget to edit me!##", verbose_name='Sidebar')),
                ('sidebar_processed', models.TextField()),
                ('footer', models.TextField(blank=True, default="###Don't forget to edit me!###", verbose_name='Footer')),
                ('footer_processed', models.TextField()),
                ('truncate_word_limit', models.IntegerField(default=200, verbose_name='Truncate word limit')),
                ('page_size', models.IntegerField(default=15, verbose_name='Page size')),
            ],
            options={
                'verbose_name': 'Website Configuration',
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stem.Post', verbose_name='Post'),
        ),
    ]
