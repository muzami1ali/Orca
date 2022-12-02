# Generated by Django 4.1.3 on 2022-12-02 21:28

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='bankTransfers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice', models.CharField(max_length=40)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('Account_Number', models.CharField(max_length=8)),
                ('Sort_Code', models.CharField(max_length=6)),
                ('Amount', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_name', models.CharField(choices=[('PIANO_PRACTICE', 'Piano Practice'), ('TRUMPET_TRAINING', 'Trumpet Training'), ('MUSIC_THEORY', 'Music Theory'), ('PERFORMANCE_PREP', 'Performance Preparation')], default='MUSIC_THEORY', max_length=50)),
                ('student_availability', models.CharField(choices=[('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday'), ('SUN', 'Sunday')], default='MON', max_length=9)),
                ('number_of_lessons', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Must complete at least one lesson.'), django.core.validators.MaxValueValidator(10, message='Maximum number of lessons exceeded. Messons per term is 10')])),
                ('interval', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Interval period between lessons must be at least 1 week.'), django.core.validators.MaxValueValidator(2, message='Maximum interval period between lessons of 2 weeks not selected.')])),
                ('duration', models.PositiveSmallIntegerField(choices=[(30, 30), (45, 45), (60, 60)], default=30)),
                ('term_period', models.CharField(choices=[('TERM1', 'Term 1'), ('TERM2', 'Term 2'), ('TERM3', 'Term 3'), ('TERM4', 'Term 4'), ('TERM5', 'Term 5'), ('TERM6', 'Term 6')], default='TERM1', max_length=6)),
                ('additional_information', models.CharField(blank=True, max_length=200, null=True, validators=[django.core.validators.MaxLengthValidator(200)])),
            ],
        ),
        migrations.CreateModel(
            name='LessonRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_authorised', models.BooleanField(default=False)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.lesson')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
