# Generated by Django 5.0.3 on 2024-03-19 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_course_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='cover',
            field=models.ImageField(default='https://dummyimage.com/400x225', upload_to='media/covers/'),
        ),
    ]
