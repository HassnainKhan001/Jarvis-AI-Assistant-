"""
URL configuration for jarvis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', TemplateView.as_view(template_name='jarvis_hud_dashboard.html'), name='index'),
    path('hud/', TemplateView.as_view(template_name='jarvis_hud_dashboard.html'), name='hud'),
    path('ultimate/', TemplateView.as_view(template_name='ultimate_professional_jarvis.html'), name='ultimate'),
    path('face/', TemplateView.as_view(template_name='professional_face_detector.html'), name='face'),
    path('voice/', TemplateView.as_view(template_name='simple_voice_interface.html'), name='voice'),
    path('helmet/', TemplateView.as_view(template_name='ironman_helmet_advanced.html'), name='helmet'),
    path('exact/', TemplateView.as_view(template_name='exact_dashboard.html'), name='exact'),
    path('professional/', TemplateView.as_view(template_name='ironman_professional.html'), name='professional'),
    path('classic/', TemplateView.as_view(template_name='index.html'), name='classic'),
]
