# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-23 10:56
from __future__ import unicode_literals

from django.db import migrations, IntegrityError
from django.contrib.contenttypes.models import ContentType
from scripts.models import Script, ScriptPermission
from django.contrib.auth.models import Permission


def add_owners(apps, schema_editor, with_create_permissions=True):
    try:
        perm_own = Permission.objects.get(
            codename='script_own',
            content_type=ContentType.objects.get_for_model(Script))
    except Permission.DoesNotExist:
        if with_create_permissions:
            # Manually run create_permissions
            from django.contrib.auth.management import create_permissions
            apps.models_module = True
            create_permissions(apps, verbosity=0)
            apps.models_module = None
            return add_owners(apps, schema_editor, with_create_permissions=False)
        else:
            raise

    for scr in Script.objects.all():
        try:
            ScriptPermission.objects.create(script=scr,
                user=scr.author,
                permission=perm_own)
        except IntegrityError:
            pass

class Migration(migrations.Migration):

    dependencies = [
        ('scripts', '0004_auto_20160323_1044'),
    ]

    operations = [
        migrations.RunPython(add_owners),
    ]
