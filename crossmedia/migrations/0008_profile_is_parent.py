# Generated by Django 2.2.3 on 2019-07-30 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crossmedia', '0007_likepost'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_parent',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]