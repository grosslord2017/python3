# Generated by Django 4.0.2 on 2022-02-04 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='product',
            name='author',
            field=models.CharField(default='', max_length=100),
        ),
    ]
