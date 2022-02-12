# Generated by Django 3.2.2 on 2021-05-12 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entreprenuer',
            fields=[
                ('fullname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=100)),
                ('mobileno', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'entreprenuers',
            },
        ),
        migrations.CreateModel(
            name='EntreprenuerContact',
            fields=[
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=100)),
                ('query', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'entreprenuercontact',
            },
        ),
    ]
