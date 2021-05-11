from django.urls import path, include
from . import views

urlpatterns = [
    # path('api-auth/', include('rest_framework.urls')),
    path('clients/', views.ClientList.as_view()),
    # path('clients/<int:pk>/', views.ClientDetail.as_view()),
#     path('contracts/', views.ContractList.as_view()),
#     path('contracts/<int:pk>/', views.ContractDetail.as_view()),
#     path('event/', views.EventList.as_view()),
#     path('events/<int:pk>/', views.EventDetail.as_view()),
]