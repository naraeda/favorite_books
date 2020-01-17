# Generated by Django 2.2.6 on 2020-01-17 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0003_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='uploaded_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='uploaded_books', to='login_app.User'),
        ),
    ]