# Generated by Django 4.2.7 on 2023-12-02 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0010_alter_commentlike_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentlike',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_likes', to='insta.profile'),
        ),
        migrations.AlterField(
            model_name='commentlike',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_likes', to='insta.comment'),
        ),
        migrations.AlterField(
            model_name='momentlike',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moment_likes', to='insta.profile'),
        ),
        migrations.AlterField(
            model_name='momentlike',
            name='moment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moment_likes', to='insta.moment'),
        ),
    ]
