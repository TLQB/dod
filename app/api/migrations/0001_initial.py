# Generated by Django 3.2.6 on 2023-05-27 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=50)),
                ('is_mailauth_completed', models.BooleanField(default=0)),
                ('is_master', models.BooleanField(default=0)),
                ('is_enabled', models.BooleanField(default=1)),
                ('config', models.JSONField(null=True)),
                ('is_super', models.BooleanField(default=0)),
            ],
            options={
                'db_table': 'admins',
            },
        ),
    ]
