from django.db import models
from vendor.models import Vendor
from global_methods.common_methods import CommonGlobalMethods as CGM
from django.db.models.signals import pre_save
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

_cgm=CGM()


class PurchaseOrderTracking(models.Model):
    po_number=models.CharField(max_length=50, unique=True, db_index=True, editable=False)
    vendor=models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True, related_name="vendor_order")
    order_date=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    delivery_date=models.DateTimeField(null=True,blank=True)
    on_time_delivery_date=models.DateTimeField(null=True,blank=True)
    items = models.JSONField(null=True, blank=True)
    quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default="pending", null=True, blank=True)
    quality_rating = models.FloatField(null=True, default=0)
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    
class PerformanceMetrices(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="performance_metrix")
    date = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    on_time_delivery_rate = models.FloatField(null=True, default=True)
    quality_rating_avg = models.FloatField(null=True, default=True)
    average_response_time = models.DurationField(null=True, default=True)
    fulfillment_rate = models.FloatField(null=True, default=True)



def pre_save_receiver(sender, instance, *args, **kwargs): 
    if not instance.po_number: 
       instance.po_number = _cgm.generate_unique_po_number()
pre_save.connect(pre_save_receiver, sender = PurchaseOrderTracking) 