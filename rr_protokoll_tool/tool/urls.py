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
            path('starter/', include([
                path('', views.edit_starter, name='edit_starter'),
                path('delete/<programmpunkt>/', views.delete_starter)
            ])),
            path('kundschafter/', include([
                path('', views.edit_kundschafter, name='edit_kundschafter'),
                path('delete/<programmpunkt>/', views.delete_kundschafter)
            ])),
            path('pfadfinder/', include([
                path('', views.edit_pfadfinder, name='edit_pfadfinder'),
                path('delete/<programmpunkt>/', views.delete_pfadfinder)
            ])),
        ])),
    ]))
]
