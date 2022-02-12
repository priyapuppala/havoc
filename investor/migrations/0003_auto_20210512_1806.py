# Generated by Django 3.2.2 on 2021-05-12 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investor', '0002_auto_20210512_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investorprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='investorprofile',
            name='fullname',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='investorprofile',
            name='location',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='investorprofile',
            name='mobile',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
