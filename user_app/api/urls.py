from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from user_app.api.views import *
urlpatterns=[
	path('login/', obtain_auth_token, name = "login"),
	path('logout/', logout_view, name = "logout"),
	path('register/', registration_view , name = 'registration'),

]