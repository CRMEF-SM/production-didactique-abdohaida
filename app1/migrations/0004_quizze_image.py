# Generated by Django 3.2.13 on 2022-06-14 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_auto_20220609_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizze',
            name='image',
            field=models.ImageField(default='image', upload_to='img/Quizze'),
        ),
    ]
