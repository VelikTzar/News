# Generated by Django 4.0.3 on 2022-04-10 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_newssite_relevant_section_html'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='image',
        ),
    ]
