# Generated by Django 5.0 on 2023-12-27 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0018_remove_moment_liked_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='subscription_date',
            new_name='creation_date',
        ),
    ]
