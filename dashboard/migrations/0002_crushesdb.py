# Generated by Django 4.2.8 on 2024-01-05 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crushesdb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitter_name', models.CharField(blank=True, max_length=800, null=True)),
                ('submitter_email', models.CharField(blank=True, max_length=800, null=True)),
                ('crush_name', models.CharField(blank=True, max_length=800, null=True)),
                ('crush_email', models.CharField(blank=True, max_length=800, null=True)),
            ],
        ),
    ]
