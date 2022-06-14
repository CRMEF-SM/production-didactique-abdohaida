# Generated by Django 3.2.13 on 2022-06-09 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_auto_20220604_1335'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapitre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titreChapitre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Partie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titrePartie', models.CharField(max_length=100)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Cours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titreCours', models.CharField(max_length=100)),
                ('image', models.ImageField(default='image', upload_to='img/cours')),
                ('description', models.TextField()),
                ('chapitres', models.ManyToManyField(to='app1.Chapitre')),
            ],
        ),
        migrations.AddField(
            model_name='chapitre',
            name='parties',
            field=models.ManyToManyField(to='app1.Partie'),
        ),
    ]