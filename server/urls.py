from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegisterView,
    LoginView,
    TokenValidateView,
    NoteView,
    NoteCreateView,
    NoteDetailView
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('token_validate/', TokenValidateView().as_view()),
    path('notes/', NoteView.as_view()),
    path('notes/create/', NoteCreateView.as_view()),
    path('notes/update/<int:pk>/', NoteDetailView.as_view()),
    path('notes/delete/<int:pk>/', NoteDetailView.as_view())
]