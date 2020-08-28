from django.urls import path
from .views import AuthCheckView

urlpatterns = [
    path('', AuthCheckView.as_view(), name='auth-check'),
    path('<int:rid>/', AuthCheckView.as_view(), name='auth-check-detail'),

]
