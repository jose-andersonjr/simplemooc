# Generated by Django 4.0.2 on 2022-08-01 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='thread',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='forum.thread', verbose_name='Tópico'),
        ),
    ]
