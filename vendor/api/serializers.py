from rest_framework.serializers import ModelSerializer
from vendor.models import Vendor

class VendorAPISerializer(ModelSerializer):
    """
    THIS IS THE BLOG API VIEW SERILIZER VIEW...
    """

    class Meta:
        model = Vendor
        fields = [
            "name",
            "contact_details",
            "vendor_code",
            "address",
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate",
            "created_at",
            "updated_at"
        ]

    def create(self, validated_data):
        return Vendor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.contact_details = validated_data.get("contact_details", instance.contact_details)
        instance.address = validated_data.get("address", instance.address)
        instance.on_time_delivery_rate = validated_data.get("on_time_delivery_rate", instance.on_time_delivery_rate)
        instance.average_response_time = validated_data.get("average_response_time", instance.average_response_time)
        instance.fulfillment_rate = validated_data.get("fulfillment_rate", instance.fulfillment_rate)
        instance.save()
        return instance