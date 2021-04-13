from django.urls import path
from .views import DemoLoginView, DashboardView, AboutView, UserListView, user_detail_view #, UserDetailView

urlpatterns = [
    path('personel/', UserListView.as_view(), name='user_list'),
    path('personel/<str:username>/', user_detail_view, name='user_detail'),
   # path('personel/<str:username>/', UserDetailView.as_view(), name='user_detail'),
    path('about/', AboutView.as_view(), name='about'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('demo-login/', DemoLoginView.as_view(), name='demo_login')

]
