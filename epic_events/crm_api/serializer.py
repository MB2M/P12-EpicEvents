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
        model = Contract
        fields = '__all__'
        extra_kwargs = {
            'date_created': {'read_only': True},
            'date_updated': {'read_only': True},
            }

class EventSerializer(serializers.ModelSerializer):
    # contract = ContractSerializer()

    class Meta:
        model = Event
        fields = ['id', 'support_contact', 'event_status', 'attendees', 'event_date', 'notes', 'date_created', 'date_updated', 'contract']
        extra_kwargs = {
            'date_created': {'read_only': True},
            'date_updated': {'read_only': True},
            }

    def create(self, validated_data):
        contract_id = validated_data.pop('contract').id
        event = Event.objects.create(**validated_data)
        Contract.objects.filter(id=contract_id).update(event=event)
        return event

