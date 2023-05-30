from django.urls import re_path
from team_app.views import TeamView

urlpatterns = [
    re_path(r"^create_team/", TeamView.as_view({"post" : "create_team"})),
    re_path(r"^list_teams/", TeamView.as_view({"get" : "list_teams"})),
    re_path(r"^describe_team/", TeamView.as_view({"get" : "describe_team"})),
    re_path(r"^update_team/", TeamView.as_view({"post" : "update_team"})),
    re_path(r"^add_users_to_team/", TeamView.as_view({"post" : "add_users_to_team"})),
    re_path(r"^remove_users_from_team/", TeamView.as_view({"post" : "remove_users_from_team"})),
    re_path(r"^list_team_users/", TeamView.as_view({"get" : "list_team_users"})),

]