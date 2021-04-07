
from django.urls import path
from .views import (
    ProjectListView,
    ProjectCreateView,
    ProjectDetailView,
    ProjectUpdateView,
    ProjectDeleteView,
    AddTicketToProjectView
)
urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('new/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('<int:pk>/add-ticket', AddTicketToProjectView.as_view(), name='add_ticket_to_project'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_edit'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
]

