# Generated by Django 3.0.7 on 2020-06-22 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='importance',
            field=models.CharField(blank=True, choices=[('l', 'low'), ('m', 'medium'), ('h', 'high')], default='m', help_text='Importance of the task', max_length=1),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(blank=True, choices=[('o', 'ongoing'), ('f', 'finished'), ('p', 'paused'), ('a', 'abandoned')], default='o', help_text='Status of the task', max_length=1),
        ),
    ]