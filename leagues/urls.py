from django.urls import path

from .views import dashboard, team_create, team_delete, team_edit, team_list

urlpatterns = [
    path("", dashboard, name="leagues-dashboard"),
    path("teams/", team_list, name="team-list"),
    path("teams/add/", team_create, name="team-create"),
    path("teams/<int:pk>/edit/", team_edit, name="team-edit"),
    path("teams/<int:pk>/delete/", team_delete, name="team-delete"),
]


