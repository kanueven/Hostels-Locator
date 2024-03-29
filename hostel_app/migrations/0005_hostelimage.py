# Generated by Django 4.1.7 on 2023-03-27 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0004_remove_service_cost'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostelImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostel_app.hostel')),
            ],
            options={
                'verbose_name': 'HostelImage',
                'verbose_name_plural': 'HostelImages',
            },
        ),
    ]
