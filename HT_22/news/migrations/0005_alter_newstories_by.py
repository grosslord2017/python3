# Generated by Django 3.2.9 on 2022-02-02 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_newstories_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newstories',
            name='by',
            field=models.CharField(default='', max_length=200),
        ),
    ]