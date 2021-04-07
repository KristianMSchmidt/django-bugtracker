from django.urls import path
from .views import ProjectListView, ProjectDetailView, ProjectTicketCreateView

urlpatterns = [
    path('',ProjectListView.as_view(), name='project_list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    #path('<int:pk>/newticket', ProjectTicketCreateView.as_view(), name='add_ticket_to_project'),

]
