# Generated by Django 5.1.4 on 2025-01-01 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_courses_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(related_name='students', to='api.courses'),
        ),
    ]
