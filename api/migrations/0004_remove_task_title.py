# Generated by Django 3.2.3 on 2021-05-29 22:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210529_2239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='title',
        ),
    ]
