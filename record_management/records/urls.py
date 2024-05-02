from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('', views.document_list, name='document_list'),
    path('add/', views.add_document, name='add_document'),
    path('edit/<str:doc_key>/', views.edit_document, name='edit_document'),
    path('delete/<str:doc_key>/', views.delete_document, name='delete_document'),
]

