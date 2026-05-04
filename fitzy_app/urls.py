from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.handle_login, name='handle_login'),
    path('signup/', views.handle_signup, name='handle_signup'),
    path('logout/', views.handle_logout, name='handle_logout'),
    path('UserInfo/', views.user_info_form, name='user_info_form'),
    path('updateInfo/<str:path>/', views.handle_update, name='handle_update'),
    path('CalculateCalorie/', views.handle_calorie, name='handle_calorie'),
    path('CalculateProtein/', views.handle_protein, name='handle_protein'),
    path('CalculateBmi/', views.handle_bmi, name='handle_bmi'),
    path('DeleteItem/<str:item_name>/<str:path>', views.handle_delete, name='handle_delete'),
    path('delete/', views.delete_account, name='delete_account')
]
