# Generated by Django 2.0.2 on 2018-04-20 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_manager', '0003_auto_20180420_1152'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Files',
            new_name='ExportFiles',
        ),
    ]