from django.urls import path
from accounts.views import *

urlpatterns = [
	path('signup/',register_user,name = 'signup'),
	path('login/',login_user,name = 'login'),
	path('logout/',logout_user,name='logout'),
	path('',ProductSerializersView.as_view()),
	path('<int:pk>/',ProductIDSerializersView.as_view()),
	path('register/',AuthUserRegistrationView.as_view()),
]

