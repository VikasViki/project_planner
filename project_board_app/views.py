import json
from datetime import datetime
from django.http.response import JsonResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets

from project_board_app.project_board_base import ProjectBoardBase

from project_board_app.models import ProjectBoardModel, TaskModel
from team_app.models import TeamModel
from user_app.models import UserModel

from utils import *

class ProjectBoardView(viewsets.ViewSet, ProjectBoardBase):

    def create_board(self, request: str):
        response = {}
        try:
            request_data = request.data
            board_name = request_data.get("name")
            description = request_data.get("description")
            team_id = request_data.get("team_id")

            ## TODO: board name check
            if not description_length_validation(description):
                raise ValueError("description should be less than {DESCRIPTION_MAX_LENGTH} characters")

            team_record = TeamModel.objects.get(team_id=team_id)
            
            board_record = ProjectBoardModel.objects.create(board_name=board_name, description=description, team=team_record)

            print(f"Board created with id : {board_record.board_id}")
            response = {"id" : board_record.board_id}
        
        except ObjectDoesNotExist:
            response["error_message"] = f"No team exists with {team_id} team_id"
        
        except Exception as e:
            response["exception"] = str(e)
            print(f"Error in creating board. Exc: {e}")
        
        return JsonResponse(response)


    def close_board(self, request: str) -> str:
        response = {}
        try:
            request_data = request.data
            board_id = request_data.get("id")

            board_record = ProjectBoardModel.objects.get(board_id=board_id)

            if board_record.board_status == board_record.CLOSED:
                message = f"Board:{board_id} is already closed at {board_record.completion_time}"
            
            else:
                board_record.board_status = board_record.CLOSED
                board_record.completion_time = datetime.now()
                board_record.save()

                message = f"Board:{board_id} is closed at {board_record.completion_time}"
            
            response["message"] = message

        except ObjectDoesNotExist as e:
            response["error_message"] = f"board with {board_id} does not exist"
            response["exception"] = str(e)

        except Exception as e:
            response["exception"] = str(e)
            print(f"Error in exporting board. Exc: {e}")
        
        return JsonResponse(response)


    def add_task(self, request: str) -> str:
        response = {}
        try:
            request_data = request.data
            board_name = request_data.get("title")
            description = request_data.get("description")
            team_id = request_data.get("team_id")
            user_id = request_data.get("user_id")

            user_record = UserModel.objects.get(user_id=user_id)
            team_record = TeamModel.objects.get(team_id=team_id)
            board_record = ProjectBoardModel.objects.get(board_name=board_name)

            task_record = TaskModel.objects.create(task_title=board_name, task_description=description, user=user_record, team=team_record)

            board_record.tasks.add(task_record)

            message = f"Task created in {board_name} board for user:{user_id} of team:{team_id}"
            response["message"] = message
        
        except ObjectDoesNotExist as e:
            response["error_message"] = f"User, Team and Board must be created before creating task"
            response["exception"] = str(e)
        
        except Exception as e:
            response["exception"] = str(e)
            print(f"Error in adding task to board. Exc: {e}")
        
        return JsonResponse(response)


    def update_task_status(self, request: str):
        response = {}
        try:
            request_data = request.data
            task_id = request_data.get("id")
            task_status = request_data.get("status")

            task_record = TaskModel.objects.get(task_id=task_id)

            if task_status in task_record.TASK_STATUS_CHOICES:
                task_record.task_status = task_status
                task_record.save()
            else:
                raise ValueError(f"invalid task status, please select from {task_record.TASK_STATUS_CHOICES}")

            message = f"status of task:{task_id} is changed to {task_status}"
            response["message"] = message
        
        except ObjectDoesNotExist as e:
            response["error_message"] = f"Task with task_id:{task_id} does not exist"
        
        except Exception as e:
            response["exception"] = str(e)
            print(f"Error in updating task status. Exc: {e}")
        
        return JsonResponse(response)


    def list_boards(self, request: str) -> str:
        response = {}
        try:
            request_data = request.data
            team_id = request_data.get("id")

            boards_list = []

            for board in ProjectBoardModel.objects.filter(team_id=team_id, board_status=ProjectBoardModel.OPEN):
                board_dict = {
                    "id": board.board_id,
                    "name": board.board_name
                }
                boards_list += [board_dict]
            
            response = boards_list
        
        except Exception as e:
            response["exception"] = str(e)
            print(f"Error in listing boards. Exc: {e}")
        
        return JsonResponse(response, safe=False)


    def export_board(self, request: str) -> str:
        response = {}
        try:
            request_data = request.data
            board_id = request_data.get("id")

            board_record = ProjectBoardModel.objects.get(board_id=board_id)
            tasks_data_list = []
            for task in board_record.tasks.all():
                task_dict = task.__dict__
                task_dict.pop('_state', None)
                tasks_data_list += [task_dict]
            
            board_dict = board_record.__dict__
            board_dict.pop('_state', None)
            response = board_dict

            response["tasks"] = tasks_data_list
            
            ## saving json file
            file_path = f"{settings.BASE_DIR}/out/board_{board_id}_report_{datetime.now()}.json"
            
            with open(file_path, 'w') as json_file:
                json.dump(response, json_file, default=str)
            
            response = {"out": file_path}
        
        except Exception as e:
            response = {"exception" : str(e)}
            print(f"Error in exporting board. Exc: {e}")
        
        return JsonResponse(response)

    

