# Generated by Django 4.2.6 on 2024-05-16 07:00

import common.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('custom_user_management', '0001_initial'),
        ('common', '0002_delete_uploadedfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=common.models.upload_to)),
                ('file_type', models.CharField(blank=True, choices=[('Promo', 'Promotion'), ('Ardoise', 'Ardoise')], max_length=10)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('store_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='common_uploaded_files', to='custom_user_management.corak_api_userprofile')),
            ],
        ),
    ]
