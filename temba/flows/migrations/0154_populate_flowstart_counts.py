# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-04 19:12
from __future__ import unicode_literals

from django.db import migrations


def backfill_flowstart_counts(FlowRun, FlowStart, FlowStartCount):
    # for every start
    for start_id in FlowStart.objects.all().order_by('id').values_list('id', flat=True):
        count = FlowRun.objects.filter(start_id=start_id).count()
        FlowStartCount.objects.create(start_id=start_id, count=count, is_squashed=True)
        print("start %d populated with %d runs" % (start_id, count))


def apply_manual():
    from temba.flows.models import FlowRun, FlowStart, FlowStartCount
    backfill_flowstart_counts(FlowRun, FlowStart, FlowStartCount)


def apply_as_migration(apps, schema_editor):
    FlowRun = apps.get_model('flows', 'FlowRun')
    FlowStart = apps.get_model('flows', 'FlowStart')
    FlowStartCount = apps.get_model('flows', 'FlowStartCount')
    backfill_flowstart_counts(FlowRun, FlowStart, FlowStartCount)


class Migration(migrations.Migration):

    dependencies = [
        ('flows', '0153_flowstartcount'),
    ]

    operations = [
        migrations.RunPython(apply_as_migration)
    ]