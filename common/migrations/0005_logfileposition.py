# Generated by Django 4.2.6 on 2024-06-18 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_logentry'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogFilePosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_file', models.CharField(max_length=255, unique=True)),
                ('position', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
