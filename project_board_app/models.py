from email.policy import default
import imp
from statistics import mode
from django.db import models

from user_app.models import UserModel
from team_app.models import TeamModel


class TaskModel(models.Model):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    TASK_STATUS_CHOICES = { OPEN, IN_PROGRESS ,COMPLETE}

    task_id = models.AutoField(primary_key=True)
    task_title =  models.CharField(max_length=64)
    task_description = models.CharField(max_length=128)
    task_status = models.CharField(default=OPEN, max_length=20)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    team = models.ForeignKey(TeamModel, on_delete=models.CASCADE, default=None)
    creation_time = models.DateTimeField(auto_now_add=True)


class ProjectBoardModel(models.Model):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    BOARD_STATUS_CHOICES = {OPEN, CLOSED}

    board_id = models.AutoField(primary_key=True)
    board_name = models.CharField(unique=True, max_length=64)
    description = models.CharField(max_length=128)
    board_status = models.CharField(default=OPEN, max_length=20)
    team = models.ForeignKey(TeamModel, on_delete=models.CASCADE)
    tasks = models.ManyToManyField(TaskModel, default=None, related_name="tasks")
    completion_time = models.DateTimeField(null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    
