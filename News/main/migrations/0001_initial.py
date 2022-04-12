# Generated by Django 4.0.3 on 2022-04-08 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.URLField(blank=True, null=True)),
                ('url', models.URLField()),
                ('content', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
