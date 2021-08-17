
from django.urls import path
from .views import (
    ProjectListView,
    ProjectCreateView,
    ProjectDetailView,
    ProjectUpdateView,
    ProjectDeleteView,
    manage_enrollments_view
)
from tickets.views import TicketCreateView

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('manage-enrollments/', manage_enrollments_view, name='manage-enrollments'),
    path('new/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('<int:pk>/add-ticket', TicketCreateView.as_view(),
         name='add_ticket_to_project'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_edit'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
]
