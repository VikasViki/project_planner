from django.urls import re_path
from .views import UserView

urlpatterns = [
    re_path(r"^create_user/", UserView.as_view({"post" : "create_user"})),
    re_path(r"^list_users/", UserView.as_view({"get" : "list_users"})),
    re_path(r"^describe_user/", UserView.as_view({"get" : "describe_user"})),
    re_path(r"^update_user/", UserView.as_view({"post" : "update_user"})),
    re_path(r"^get_user_teams/", UserView.as_view({"get" : "get_user_teams"})),

]