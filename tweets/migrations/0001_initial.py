# Generated by Django 4.1.7 on 2023-03-30 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(default='', max_length=70)),
                ('data', models.JSONField()),
            ],
        ),
    ]
