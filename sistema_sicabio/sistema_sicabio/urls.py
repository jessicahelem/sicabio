"""sistema_sicabio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static

from sicabio import views
from sistema_sicabio import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.do_login),
    path("logout/", views.logout_user),
    path('login/submit', views.submit_login),
    path('Home',views.list_all_pacientes),
    url(r'^paciente/create/$', views.paciente_create, name='create-paciente'),
    url(r'^paciente/(?P<pk>\w{0,50})/update/$', views.paciente_update, name='paciente_update'),
    url(r'^pacientes/$', views.list_all_pacientes, name='paciente_list'),
    path('pacientes/excluir_paciente/<id>/', views.delete_paciente),
    # path('pacientes/<id>/adicionar-digitais/submit', views.set_digitais),
    path('pacientes/<id>/digitais/', views.listarImpressoes),
    # url(r'^pacientes/(?P<id>\w{0,50})/adicionar-digitais/$', views.ViewImpressao.as_view(), name='view-impresssao'),
    # url(r'^ajax/(?P<id>\w{0,50})/adicionar-digitais/$',views.BasicUploadView, name='basic_upload'),
    url(r'^pacientes/(?P<id>\w{0,50})/digitais/create', views.post, name='create-impressao'),
    path('pacientes/<id>/digitais/delete_impressao/<int:id_impressao>/', views.delete_impressao),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)