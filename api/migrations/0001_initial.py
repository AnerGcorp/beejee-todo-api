# Generated by Django 3.2.3 on 2021-05-29 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('status', models.IntegerField(choices=[(0, 'задача не выполнена'), (1, 'задача не выполнена, отредактирована админом'), (10, 'задача выполнена'), (11, 'задача отредактирована админом и выполнена')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=500)),
                ('token', models.CharField(max_length=255)),
            ],
        ),
    ]
