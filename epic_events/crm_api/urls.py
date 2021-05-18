from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api-auth/', include('rest_framework.urls')),
    path('clients/', views.ClientList.as_view()),
    path('clients/<int:client>/', views.ClientDetail.as_view()),
    path('clients/<int:client>/contracts/', views.ContractList.as_view()),
    path('clients/<int:client>/contracts/<int:id>/', views.ContractDetail.as_view()),
    path('clients/<int:client>/contracts/<int:contract>/events/', views.EventList.as_view()),
    path('clients/<int:client>/contracts/<int:contract>/events/<int:id>/', views.EventDetail.as_view()),
]