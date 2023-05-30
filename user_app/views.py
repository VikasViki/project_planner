
from rest_framework import viewsets

from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from user_app.user_base import UserBase
from user_app.models import UserModel
from utils import *

class UserView(viewsets.ViewSet, UserBase):

   def create_user(self, request: str) -> str:
      response = {}

      try:
         request_data = request.data
         
         user_name = request_data.get("name")
         if is_empty(user_name):
            raise ValueError(f"user_name should not be empty")

         if not user_name_length_validation(user_name):
            raise ValueError(f"{user_name} should be less than {USER_NAME_MAX_LENGTH} characters")

         display_name = request_data.get("display_name")
         display_name_validaton(display_name)

         user_record = UserModel.objects.create(user_name=user_name, display_name=display_name)
         
         print(f"User created with id : {user_record.user_id}")
         response = {"id" : user_record.user_id}

      except Exception as e:
         response["exception"] = str(e)
         print(f"Error in creating user. Exc: {e}")
      
      return JsonResponse(response)
   
   def list_users(self, request: str) -> str:
      response = {}

      try:
         users_list = []
         
         for user in UserModel.objects.all():
            user_dict = {
               "name" : user.user_name,
               "display_name" : user.display_name,
               "creation_time" :  f"{user.creation_time:%Y-%m-%d %H:%M:%S%z}"
               }
            users_list += [user_dict]
         
         response = users_list

      except Exception as e:
         response["exception"] = str(e)
         print(f"Error in listing users. Exc: {e}")
      
      return JsonResponse(response, safe=False)
   
   def describe_user(self, request: str) -> str:
      response = {}

      try:
         request_data = request.data
         user_id = request_data.get("id")
         if is_empty(user_id):
            raise ValueError(f"user_id should not be empty")
         
         user = UserModel.objects.get(user_id=user_id)

         response = {
            "name" : user.user_name,
            "description" : user.description,
            "creation_time" : user.creation_time
            }
      
      except ObjectDoesNotExist:
         response["error_message"] = f"No user exists with {user_id} user_id"
      
      except Exception as e:
         response["exception"] = str(e)
         print(f"Error in listing users. Exc: {e}")
      
      return JsonResponse(response)
   
   def update_user(self, request: str) -> str:
      response = {}

      try:
         request_data = request.data
         user_id = request_data.get("id")
         if is_empty(user_id):
            raise ValueError(f"user_id should not be empty")
         
         request_user = request_data.get("user")
         if not request_user:
            raise ValueError(f"user data should not be empty")
         
         request_user_name = request_user.get("name")
         request_display_name = request_user.get("display_name")
         display_name_validaton(request_display_name)

         user = UserModel.objects.get(user_id=user_id)
         if user.user_name != request_user_name:
            raise ValueError( f"user name cannot be updated")
         
         user.display_name = request_display_name
         user.save()

         message = f"Display name updated to {request_display_name} for user: {user_id}"
         print(message)
         response = {"message": message}
      
      except ObjectDoesNotExist:
         response["error_message"] = f"No user exists with {user_id} user_id"
      
      except Exception as e:
         response["exception"] = str(e)
         print(f"Error in updating users. Exc: {e}")
      
      return JsonResponse(response)
   
   def get_user_teams(self, request: str) -> str:
      response = {}
      try:
         request_data = request.data
         user_id = request_data.get("id")

         teams_list = []

         user_record = UserModel.objects.get(user_id=user_id)
         for team in user_record.users.all():
            team_dict = {
               "name" : team.team_name,
               "description" : team.description,
               "creation_time" : team.creation_time
               }
            teams_list += [team_dict]
         
         response = teams_list
      
      except Exception as e:
         response["exception"] = str(e)
         print(f"Error in getting user teams. Exc: {e}")
      
      return JsonResponse(response, safe=False)