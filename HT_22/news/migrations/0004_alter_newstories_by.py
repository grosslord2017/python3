# Generated by Django 3.2.9 on 2022-01-31 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_jobstories_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newstories',
            name='by',
            field=models.TextField(default=''),
        ),
    ]
