# Generated by Django 4.1.3 on 2023-01-09 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
    ]