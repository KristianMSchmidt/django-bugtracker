from django.urls import path
from .views import DashboardView, UserListView, UserDetailView

urlpatterns = [
    path('personel/', UserListView.as_view(), name='user_list'),
    path('personel/<str:username>/', UserDetailView.as_view(), name='user_detail'),
    path('', DashboardView.as_view(), name='dashboard'),
]
