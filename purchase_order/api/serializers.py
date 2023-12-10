
from rest_framework.serializers import ModelSerializer
from purchase_order.models import PurchaseOrderTracking, PerformanceMetrices
from rest_framework import serializers

class PurchaseOrderSerializer(ModelSerializer):
    vendor = serializers.SerializerMethodField()
    
    class Meta:
        model = PurchaseOrderTracking
        
        fields = [
            "po_number",
            "vendor",
            "order_date",
            "delivery_date",
            "on_time_delivery_date",
            "items",
            "quantity",
            "status",
            "quality_rating",
            "issue_date",
            "acknowledgment_date"
        ]

    def create(self, validated_data):
        return PurchaseOrderTracking.objects.create(**validated_data)
    
    

    def update(self, instance, validated_data):
        instance.delivery_date = validated_data.get("delivery_date", instance.delivery_date)
        instance.delivery_date = validated_data.get("delivery_date", instance.delivery_date)
        instance.items = validated_data.get("items", instance.items)
        instance.quantity = validated_data.get("quantity", instance.quantity)
        instance.status = validated_data.get("status", instance.status)
        instance.quality_rating = validated_data.get("quality_rating", instance.quality_rating)
        instance.issue_date = validated_data.get("issue_date", instance.issue_date)
        instance.acknowledgment_date = validated_data.get("acknowledgment_date", instance.acknowledgment_date)
        instance.on_time_delivery_date = validated_data.get("on_time_delivery_date", instance.on_time_delivery_date)
        instance.save()
        return instance
    
    
    def get_vendor(self, obj=None):
        try:
            if obj is not None:
                return obj.vendor.name
            else:
                return None
        except Exception as e:
            return None
        

class PerformcnceMetrixSerializer(ModelSerializer):
    vendor = serializers.SerializerMethodField()
    
    class Meta:
        model = PerformanceMetrices
        
        fields = [
            "vendor",
            "date",
            "created_at",
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate"
        ]
        
    
    def get_vendor(self, obj=None):
        try:
            if obj is not None:
                return obj.vendor.name
            else:
                return None
        except Exception as e:
            return None