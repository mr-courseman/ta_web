from rest_framework import serializers
from .models import *


class PassportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = "__all__"


class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class PersonalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personal
        fields = "__all__"


class MovementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movement
        fields = "__all__"


class ToursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = "__all__"


class ContractsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"
