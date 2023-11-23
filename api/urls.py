from django.urls import path

from api.views import ACCOUNTSCreateAPIView

app_name = 'api'

urlpatterns = [
    path('test/', ACCOUNTSCreateAPIView.as_view(), name='test'),
]