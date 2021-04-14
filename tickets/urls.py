from django.urls import path
from .views import (
    TicketListView, 
    TicketCreateView,
    #TicketDetailView,
    ticket_detail_view,
    TicketUpdateView,
    TicketDeleteView,
    TicketCommentUpdateView,
    TicketCommentDeleteView
    )

urlpatterns = [
    # ticket views
    path('', TicketListView.as_view(), name='ticket_list'),
    #path('<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('<int:pk>/', ticket_detail_view, name='ticket_detail'),

    path('new/', TicketCreateView.as_view(), name='ticket_create'),
    path('<int:pk>/edit/', TicketUpdateView.as_view(), name='ticket_edit'),
    path('<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket_delete'),
    
    #ticket comment views
    path('comments/<int:pk>/edit/', TicketCommentUpdateView.as_view(), name='ticket_comment_edit'),
    path('comments/<int:pk>/delete/', TicketCommentDeleteView.as_view(), name='ticket_comment_delete'),
    ]
    
