from rest_framework.serializers import ModelSerializer
from .models import Label, CardLabel


class LabelSerializer(ModelSerializer):
    class Meta:
        model = Label
        fields = ["id", "title", "color"]
        read_only_fields = ["id"]


class CardLabelSerializer(ModelSerializer):
    class Meta:
        model = CardLabel
        fields = ["id", "card", "label"]