from django.urls import path

from api.views import ACCOUNTSCreateAPIView, SENDXRPView

app_name = 'api'

urlpatterns = [
    path('test/', ACCOUNTSCreateAPIView.as_view(), name='test'),
    path('test2/', SENDXRPView.as_view(), name='test2'),
]