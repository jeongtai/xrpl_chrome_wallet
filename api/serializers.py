from rest_framework import serializers

from api.models import ACCOUNT


class ACCOUNTSerializer(serializers.ModelSerializer):
    class Meta:
        model = ACCOUNT
        fields = ['wallet_address','private_key','public_key','balance']


class SENDXRPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ACCOUNT
        fields = ['wallet_address']


class SENDXRP(serializers.Serializer):
    sender = SENDXRPSerializer()
    receiver = SENDXRPSerializer()