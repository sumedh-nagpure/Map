from django.urls import path
from .views import DownloadImageView

urlpatterns = [
    path('api/download-image/', DownloadImageView.as_view(), name='download_image'),
]