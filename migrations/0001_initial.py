# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-16 14:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FirewallEntry',
            fields=[
                ('entry_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(max_length=15)),
                ('action', models.CharField(max_length=10)),
                ('data', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ForwardEntry',
            fields=[
                ('entry_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now=True)),
                ('dstaddress', models.CharField(max_length=15)),
                ('dstport', models.IntegerField()),
                ('srcaddress', models.CharField(max_length=15)),
                ('srcport', models.IntegerField()),
                ('proto', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('token_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('service', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='TrafficStat',
            fields=[
                ('entry_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now=True)),
                ('packets', models.IntegerField()),
                ('bytes', models.IntegerField()),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='router.Token')),
            ],
        ),
        migrations.AddField(
            model_name='forwardentry',
            name='token',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='router.Token'),
        ),
        migrations.AddField(
            model_name='firewallentry',
            name='forward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='router.ForwardEntry'),
        ),
        migrations.AddField(
            model_name='firewallentry',
            name='token',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='router.Token'),
        ),
    ]
