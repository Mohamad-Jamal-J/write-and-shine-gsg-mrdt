# Generated by Django 5.1.1 on 2024-09-30 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='education',
            field=models.CharField(default='', max_length=255),
        ),
    ]
