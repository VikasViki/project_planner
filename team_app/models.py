from django.db import models

from user_app.models import UserModel

class TeamModel(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=128, blank=True)
    admin = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(UserModel, related_name="users")


