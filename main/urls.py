from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from .import views

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('', views.task_list, name='home'),
    path('geogebra', views.view_geo, name='geogebra'),
    path('video_list', views.video_list, name="video_list"),
    path('video/<int:pk>', views.video_detail.as_view(), name="video_detail"),
    path('create/video', views.create_video, name="create_video"),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.Register.as_view(), name='register'),
    path('create', views.Create.as_view(), name='create_task'),
    path('detail/<pk>', views.DetailTask.as_view(), name='detail'),
    path('confirm_email/', TemplateView.as_view(template_name='registration/confirm_email.html'), name='confirm_email'),
    path('verify_email/<uidb64>/<token>/', views.EmailVerify.as_view(), name='verify_email'),
    path('invalid_verify/', TemplateView.as_view(template_name='registration/invalid_verify.html'), name='invalid_verify'),
path('profile', views.view_profile, name='profile'),
]