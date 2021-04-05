from django.urls import path

from . import views

urlpatterns = [
    path('chatbot/', views.chatbot, name='chat_bot'),
    path('useractions/', views.UserActions.as_view(), name='user_actions')
]