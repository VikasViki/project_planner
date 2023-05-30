from django.db import models

from django.core.validators import MaxLengthValidator

# from team_app.models import TeamModel

class UserModel(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(unique=True, max_length=64, validators=[MaxLengthValidator(64)])
    display_name = models.CharField(max_length=64, validators=[MaxLengthValidator(64)])
    description = models.CharField(max_length=128, validators=[MaxLengthValidator(128)], blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    # team = models.ForeignKey(TeamModel, on_delete=models.CASCADE, default=None, db_index=True)
