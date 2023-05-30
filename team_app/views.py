
from rest_framework import viewsets

from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from team_app.team_base import TeamBase

from team_app.models import TeamModel
from user_app.models import UserModel
from utils import *

class TeamView(viewsets.ViewSet, TeamBase):

    def create_team(self, request: str) -> str:
        response = {}

        try:
            request_data = request.data
            team_name = request_data.get("name")
            description = request_data.get("description")
            admin_user_id = request_data.get("admin")

            if not team_name_length_validation(team_name):
                raise ValueError("team_name should be less than {TEAM_NAME_MAX_LENGTH} characters")

            if not description_length_validation(description):
                raise ValueError(f"description should  be less than {DESCRIPTION_MAX_LENGTH} characters")

            # Check admin user exists
            try:
                admin_user = UserModel.objects.get(user_id=admin_user_id)
            except ObjectDoesNotExist:
                raise ValueError(f"User with id:{admin_user_id} does not exist")
            

            team_record = TeamModel.objects.create(team_name=team_name, description=description, admin=admin_user)

            print(f"Team created with id : {team_record.team_id}")
            response = {
                "id": team_record.team_id
            }
        
        except Exception as e:
            response["exception"] = str(e)
            print(f"Error in creating team. Exc: {e}")
        
        return JsonResponse(response)
    

    def list_teams(self, request) -> str:
        response = {}
        try:
            teams_list = []
            for team in TeamModel.objects.all():
                team_dict = {
                    "name" : team.team_name,
                    "description" : team.description,
                    "creation_time" : team.creation_time,
                    "admin": team.admin.user_id
                    }
                teams_list += [team_dict]
            response = teams_list
        
        except Exception as e:
            response["exception"] = str(e)
            print(f"Error in listing teams. Exc: {e}")
        
        return JsonResponse(response, safe=False)
    

    def describe_team(self, request: str) -> str:
        response = {}
        try:
            request_data = request.data
            team_id = request_data.get("id")

            team_record = TeamModel.objects.get(team_id=team_id)
            response = {
                "name" : team_record.team_name,
                "description" : team_record.description,
                "creation_time" : team_record.creation_time,
                "admin": team_record.admin.user_id
                }
        
        except ObjectDoesNotExist:
            response["error_message"] = f"No team exists with {team_id} team_id"
        
        except Exception as e:
            response["exception"] = str(e)
            print(f"Error in describing teams. Exc: {e}")
        
        return JsonResponse(response)
    

    def update_team(self, request: str) -> str:
        response = {}
        try:
            request_data = request.data
            team_id = request_data.get("id")

            requested_team = request_data.get("team")
            team_name = requested_team.get("name")
            team_description = requested_team.get("description")
            team_admin_user_id = requested_team.get("admin")

            admin_user = UserModel.objects.get(user_id=team_admin_user_id)

            team_record = TeamModel.objects.get(team_id=team_id)
            team_record.team_name = team_name
            team_record.description = team_description
            team_record.admin = admin_user
            team_record.save()

            message = f"Team {team_id} is updated"
            print(message)
            response["message"] = message
        
        except ObjectDoesNotExist:
            response["error_message"] = f"No team exists with {team_id} team_id"
        
        except Exception as e:
            response["exception"] = str(e)
            print(f"Error in updating team. Exc: {e}")
        
        return JsonResponse(response)

    
    def add_users_to_team(self, request: str):
        response = {}
        try:
            request_data = request.data
            team_id = request_data.get("id")
            users_id_list = request_data.get("users")

            team_record = TeamModel.objects.get(team_id=team_id)
            for user_id in users_id_list:
                user_record = UserModel.objects.get(user_id=user_id)
                team_record.users.add(user_record)
            team_record.save()

            message = f"{users_id_list} users added to team {team_id}"
            print(message)
            response["message"] = message
        
        except ObjectDoesNotExist:
            response["error_message"] = f"No team exists with {team_id} team_id"

        except Exception as e:
            response["exception"] = str(e)
            print(f"Error in adding users to team. Exc: {e}")
        
        return JsonResponse(response)
    

    def remove_users_from_team(self, request: str):
        response = {}
        try:
            request_data = request.data
            team_id = request_data.get("id")
            users_id_list = request_data.get("users")

            team_record = TeamModel.objects.get(team_id=team_id)
            for user_id in users_id_list:
                user_record = UserModel.objects.get(user_id=user_id)
                team_record.users.remove(user_record)
            team_record.save()

            message = f"{users_id_list} users removed from team {team_id}"
            print(message)
            response["message"] = message
        
        except ObjectDoesNotExist:
            response["error_message"] = f"No team exists with {team_id} team_id"
        
        except Exception as e:
            response["exception"] = str(e)
            print(f"Error in removing users from team. Exc: {e}")
        
        return JsonResponse(response)
    

    def list_team_users(self, request: str):
        response = {}
        try:
            users_list = []

            request_data = request.data
            team_id = request_data.get("id")
            team_record = TeamModel.objects.get(team_id=team_id)

            for user in team_record.users.all():
                user_dict = {
                    "id" : user.user_id,
                    "name" : user.user_name,
                    "display_name" : user.display_name
                    }
                users_list += [user_dict]
            
            response = users_list
        
        except ObjectDoesNotExist:
            response["error_message"] = f"No team exists with {team_id} team_id"
        
        except Exception as e:
            response["exception"] = str(e)
            print(f"Error in listing team user. Exc: {e}")
        
        return JsonResponse(response, safe=False)