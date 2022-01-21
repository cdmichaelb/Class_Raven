# Generated by Django 4.0.1 on 2022-01-14 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PokemonType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('height', models.FloatField(max_length=100, null=True)),
                ('weight', models.FloatField(max_length=100, null=True)),
                ('image_front', models.CharField(max_length=100)),
                ('image_back', models.CharField(max_length=100)),
                ('types', models.ManyToManyField(blank=True, to='pokedex_app.PokemonType')),
            ],
        ),
    ]
