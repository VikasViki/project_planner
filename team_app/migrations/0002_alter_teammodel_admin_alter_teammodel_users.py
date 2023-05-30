# Generated by Django 4.2.1 on 2023-05-30 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("user_app", "0003_alter_usermodel_description_and_more"),
        ("team_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="teammodel",
            name="admin",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="user_app.usermodel"
            ),
        ),
        migrations.AlterField(
            model_name="teammodel",
            name="users",
            field=models.ManyToManyField(
                related_name="users_teams", to="user_app.usermodel"
            ),
        ),
    ]
