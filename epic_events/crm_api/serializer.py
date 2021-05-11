from django.db.models import fields
from rest_framework import serializers
from crm.models import Client, Contract, Event

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        extra_kwargs = {
            'date_created': {'read_only': True},
            'date_updated': {'read_only': True},
            }

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model : Contract
        fiedls = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

