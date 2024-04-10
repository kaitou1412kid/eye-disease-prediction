from django.urls import path,include
from .views import UserLoginView, UserSignUpView, EyeDiseasePredictionView

urlpatterns = [
    path('signup/',UserSignUpView.as_view(),name="user-signup"),
    path('login/',UserLoginView.as_view(),name="user-login"),
    path('eyepredict/',EyeDiseasePredictionView.as_view(),name="eye-disease"),
]
