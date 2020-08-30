from django.urls import path
from .views import AuthCheckView, AuthCheckTplView

urlpatterns = [
    path('notpl', AuthCheckView.as_view(), name='auth-check'),
    path('<int:rid>/', AuthCheckView.as_view(), name='auth-check-detail'),
    path('', AuthCheckTplView.as_view(), name='auth-check-tpl'),
]
