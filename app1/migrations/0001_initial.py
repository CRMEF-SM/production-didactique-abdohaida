# Generated by Django 3.2.12 on 2022-05-21 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=30)),
                ('discription', models.TextField()),
                ('videoFile', models.FileField(null=True, upload_to='video/', verbose_name='Le video')),
            ],
        ),
    ]