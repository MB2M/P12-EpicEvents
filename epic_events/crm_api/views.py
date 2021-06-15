from django.http.response import Http404
from django.shortcuts import redirect, render
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions, IsAdminUser

from crm.models import Client, Contract, Event
from .serializer import ClientSerializer, ContractSerializer, EventSerializer
from .permissions import IsManager, IsSales, IsSupport


class ClientList(generics.ListCreateAPIView):
    """
    List all clients, or create a new client.
    """
    permission_classes = [DjangoModelPermissions]
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    filterset_fields = ['first_name', 'last_name', 'email', 'phone', 'mobile', 'compagny_name', 'propect']

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.function.name == 'sales':
            request.data._mutable = True
            request.data['sales_contact'] = user.id
            request.data._mutable = False
        return self.create(request, *args, **kwargs)

class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update or delete a Client.
    """
    permission_classes = [IsSales|IsManager]
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    lookup_url_kwarg = 'client'

    def put(self, request, *args, **kwargs):
        user = request.user
        if user.function.name == 'sales':
            request.data._mutable = True
            request.data['sales_contact'] = user.id
            request.data._mutable = False
        return super().update(request, *args, **kwargs)

class ContractList(generics.ListCreateAPIView):
    """
    List all clients, or create a new contrat.
    """
    permission_classes = [DjangoModelPermissions&IsSales|IsManager]
    serializer_class = ContractSerializer
    filterset_fields = ['status', 'amount', 'client']

    def get_queryset(self):
        client_id = self.kwargs['client']
        client = generics.get_object_or_404(Client, pk=client_id)
        self.check_object_permissions(self.request, client)
        return client.contract_set.all()

    def post(self, request, *args, **kwargs):
        user = request.user
        client_id = self.kwargs['client']
        if user.function.name == 'sales':
            request.data._mutable = True
            request.data['client'] = client_id
            request.data['sales_contact'] = user.id
            request.data._mutable = False
        return super().create(request, *args, **kwargs)

class ContractDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update or delete a Client.
    """
    permission_classes = [IsSales|IsManager]
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    multiple_lookup_fields = ['client', 'id']

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.multiple_lookup_fields:
            filter[field] = self.kwargs[field]
        obj = generics.get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


    def put(self, request, *args, **kwargs):
        client_id = self.kwargs['client']
        user = request.user
        if user.function.name == 'sales':
            request.data._mutable = True
            request.data['client'] = client_id
            request.data['sales_contact'] = user.id  # faut-il modifier le sales contact automatiquement?
            request.data._mutable = False
        return super().update(request, *args, **kwargs)

class EventList(generics.ListCreateAPIView):
    """
    List all clients, or create a new contrat.
    """
    permission_classes = [DjangoModelPermissions&IsSales|IsManager]
    serializer_class = EventSerializer
    filterset_fields = ['event_status', 'attendees', 'event_date']

    def get_queryset(self):
        client_id = self.kwargs['client']
        client = generics.get_object_or_404(Client, pk=client_id)
        contract_id = self.kwargs['contract']
        contract = generics.get_object_or_404(Contract, pk=contract_id)
        self.check_object_permissions(self.request, client)
        if Client.objects.filter(id=client.id, contract=contract).exists():
            return Event.objects.filter(contract=contract)
        else:
            raise Http404

    def post(self, request, *args, **kwargs):
        user = request.user
        contract_id = self.kwargs['contract']
        if user.function.name == 'sales':
            request.data._mutable = True
            request.data['contract'] = contract_id
            request.data['event_status'] = 1    # status planning
            request.data._mutable = False
        return super().create(request, *args, **kwargs)

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update or delete a Client.
    """
    permission_classes = [IsSales|IsManager|IsSupport]
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    multiple_lookup_fields = ['contract', 'id']

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.multiple_lookup_fields:
            filter[field] = self.kwargs[field]
        obj = generics.get_object_or_404(queryset, **filter)

        if obj.contract.client.id != self.kwargs['client']:
            raise Http404

        self.check_object_permissions(self.request, obj)
        return obj


    def put(self, request, *args, **kwargs):
        contract_id = self.kwargs['contract']
        user = request.user
        if user.function.name == 'support':
            request.data._mutable = True
            request.data['contract'] = contract_id
            request.data['support_contact'] = user.id
            request.data._mutable = False

        if user.function.name == 'sales':
            request.data._mutable = True
            request.data['contract'] = contract_id
            request.data._mutable = False

        return super().update(request, *args, **kwargs)