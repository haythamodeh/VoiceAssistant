# Generated by Django 2.1.7 on 2019-02-25 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voice_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Phrase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
            ],
        ),
    ]
