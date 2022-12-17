# Generated by Django 4.1.4 on 2022-12-17 15:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notebook', '0006_alter_comment_owner_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favourite', models.BooleanField(default=False)),
                ('notebook_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to='notebook.notebook')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
