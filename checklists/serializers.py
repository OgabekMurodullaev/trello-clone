from rest_framework.serializers import ModelSerializer
from .models import CheckList, CheckListItem


class CheckListItemSerializer(ModelSerializer):
    class Meta:
        model = CheckListItem
        fields = ["id", "checklist", "text", "is_completed"]
        read_only_fields = ["id"]


class CheckListSerializer(ModelSerializer):
    items = CheckListItemSerializer(many=True, read_only=True)

    class Meta:
        model = CheckList
        fields = ["id", "title", "card", "items"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return CheckList.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in  validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
