from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('player_register/', views.player_register.as_view(), name='player_register'),
    path('/', views.main, name='main'),
    path('home/',views.home, name='home'),
    path('level1_quiz/', views.level1_quiz,{'level': 'Level 1'}, name='level1_quiz'),
    path('level2_quiz/', views.level2_quiz,{'level': 'Level 2'}, name='level2_quiz'),
    path('rank/',views.user_scores,name='user_scores'),
    path('addQuestion/<str:level>/',views.addQuestion, name='addQuestion'),
    path('certificate/', views.certificate, name='certificate'),
    path('generate_certificate/', views.generate_certificate, name='generate_certificate'),
]