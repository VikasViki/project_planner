from django.urls import re_path

from project_board_app.views import ProjectBoardView

urlpatterns = [
    re_path(r"^create_board/", ProjectBoardView.as_view({"post": "create_board"})),
    re_path(r"^close_board/", ProjectBoardView.as_view({"post": "close_board"})),
    re_path(r"^add_task/", ProjectBoardView.as_view({"post": "add_task"})),
    re_path(r"^update_task_status/", ProjectBoardView.as_view({"post": "update_task_status"})),
    re_path(r"^list_boards/", ProjectBoardView.as_view({"get": "list_boards"})),
    re_path(r"^export_board/", ProjectBoardView.as_view({"get": "export_board"})),
]