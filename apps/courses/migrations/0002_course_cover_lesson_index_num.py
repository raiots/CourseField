# Generated by Django 5.0.3 on 2024-03-18 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='media/covers/'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='index_num',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]