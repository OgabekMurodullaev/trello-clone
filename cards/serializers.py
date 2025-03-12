from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from accounts.models import User
from .models import Card, CardMember, Attachment


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"

    def create(self, validated_data):
        return Card.objects.create(**validated_data)


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ("id", "card", "uploaded_by", "file", "uploaded_at")
        read_only_fields = ("id", "uploaded_by", "uploaded_at")

    def create(self, validated_data):
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data)


class AddMemberCardSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CardMember
        fields = ("user_id", "added_at")

    def validate_user_id(self, value):
        return get_object_or_404(User, id=value)

    def create(self, validated_data):
        user = validated_data.pop("user_id")
        card = self.context["card"]
        return CardMember.objects.create(user=user, card=card, **validated_data)