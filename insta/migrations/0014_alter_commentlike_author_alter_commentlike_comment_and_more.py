# Generated by Django 4.2.7 on 2023-12-02 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0013_remove_comment_liked_by_remove_moment_liked_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentlike',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_like_author', to='insta.profile'),
        ),
        migrations.AlterField(
            model_name='commentlike',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_comment', to='insta.comment'),
        ),
        migrations.AlterField(
            model_name='momentlike',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moment_like_author', to='insta.profile'),
        ),
        migrations.AlterField(
            model_name='momentlike',
            name='moment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_moment', to='insta.moment'),
        ),
    ]
