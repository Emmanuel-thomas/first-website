# Generated by Django 3.2.1 on 2021-07-18 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ('-created',)},
        ),
    ]