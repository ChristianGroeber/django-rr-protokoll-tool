from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('jahresplan/', views.jahresplan, name='jahresplan'),
    path('nachmittag/<nachmittag>/', views.nachmittag),
    path('nachmittag/<nachmittag>/', include([
        path('', views.nachmittag),
        path('edit/', include([
            path('starter/', views.edit_starter, name='edit_starter'),
            path('kundschafter/', views.edit_kundschafter, name='edit_kundschafter'),
            path('pfadfinder/', views.edit_pfadfinder, name='edit_pfadfinder')
        ])),
    ]))
]
