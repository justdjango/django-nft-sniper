from django.urls import path
from . import views

app_name = "sniper"

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="project-list"),
    path("create/", views.ProjectCreateView.as_view(), name="project-create"),
    path("project/<pk>/", views.ProjectDetailView.as_view(), name="project-detail"),
    path(
        "project/<pk>/update/", views.ProjectUpdateView.as_view(), name="project-update"
    ),
    path(
        "project/<pk>/delete/", views.ProjectDeleteView.as_view(), name="project-delete"
    ),
    path("project/<pk>/clear/", views.ProjectClearView.as_view(), name="project-clear"),
    path("project/<pk>/fetch-nfts/", views.FetchNFTsView.as_view(), name="fetch-nfts"),
]
