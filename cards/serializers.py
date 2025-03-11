from rest_framework import serializers
from .models import Card, CardMember

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"

    def create(self, validated_data):
        return Card.objects.create(**validated_data)


class CardMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardMember
        fields = ("user", "added_at")
