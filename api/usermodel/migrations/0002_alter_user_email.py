# Generated by Django 3.2 on 2022-03-09 10:43

import django.contrib.postgres.fields.citext
from django.contrib.postgres.operations import CITextExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermodel', '0001_initial'),
    ]

    operations = [
        CITextExtension(),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=django.contrib.postgres.fields.citext.CIEmailField(error_messages={'unique': 'A user with that username already exists.'}, max_length=254, unique=True, verbose_name='Email Address'),
        ),
    ]