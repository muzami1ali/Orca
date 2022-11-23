# Generated by Django 4.1.3 on 2022-11-23 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0003_lesson_lessonrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='term_period',
            field=models.CharField(choices=[('TERM1', 'Term 1'), ('TERM2', 'Term 2'), ('TERM3', 'Term 3'), ('TERM4', 'Term 4'), ('TERM5', 'Term 5'), ('TERM6', 'Term 6')], default='TERM1', max_length=6),
        ),
    ]