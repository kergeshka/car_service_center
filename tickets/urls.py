from django.urls import path, re_path
from .views import QueueHandler, MenuView, ProcessingView, WelcomeView, NextView
from django.views.generic import RedirectView

urlpatterns = [
    path('welcome/', WelcomeView.as_view()),
    path('menu/', MenuView.as_view(), name="menu"),
    path('get_ticket/<link>/', QueueHandler.as_view()),
    path('processing', ProcessingView.as_view()),
    path('processing/', RedirectView.as_view(url="/processing"), name="operator"),
    re_path('next/', NextView.as_view()),
]


