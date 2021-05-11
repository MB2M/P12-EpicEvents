from django.shortcuts import redirect, render
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from crm.models import Client
from .serializer import ClientSerializer


class ClientList(generics.ListCreateAPIView):
    """
    List all clients, or create a new client.
    """
    # permission_classes = [IsManager|IsSales]
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def post(self, request, *args, **kwargs):
        #TODO: ajouter automatiquement le sales_contact si le créateur est un vendeur.
        # user = request.user
        # if user.function.function == 'sales':
            # request.data._mutable = True
            # request.data['sales_contact'] = request.user.id
            # request.data._mutable = False
        return self.update(request, *args, **kwargs)

class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Update or delete an Client.
    """
    # permission_classes = [IsManager|IsSales]
    serializer_class = ClientSerializer
    queryset = Client.objects.all()