from django.urls import path
from .views import DemoLoginView, AboutView, UserListView, user_detail_view

urlpatterns = [
    path('personel/', UserListView.as_view(), name='user_list'),
    path('personel/<str:username>/', user_detail_view, name='user_detail'),
    path('about/', AboutView.as_view(), name='about'),
    path('', DemoLoginView.as_view(), name='demo_login')
]
