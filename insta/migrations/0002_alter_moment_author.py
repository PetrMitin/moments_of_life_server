# Generated by Django 4.2.7 on 2023-11-11 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moment', to='insta.profile'),
        ),
    ]
