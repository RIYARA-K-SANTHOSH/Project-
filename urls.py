from django.urls import path
from matrimonyapp import views  # Import from matrimonyapp

urlpatterns = [
    path("chatbot/", views.chatbot_response, name="chatbot"),  
]
