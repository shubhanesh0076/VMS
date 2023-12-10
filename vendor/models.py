from django.db import models
import random
import string
from django.utils.text import slugify
from django.db.models.signals import pre_save
# Create your models here.


class Vendor(models.Model):
    name=models.CharField(max_length=50, null=True, blank=True)
    contact_details=models.CharField(max_length=13, null=True, blank=True)
    vendor_code=models.CharField(max_length=50, unique=True, editable=False)
    address=models.TextField(null=True, blank=True)
    on_time_delivery_rate=models.FloatField(null=True, blank=True)
    quality_rating_avg=models.FloatField(null=True, blank=True)
    average_response_time=models.FloatField(null=True, blank=True)
    fulfillment_rate=models.FloatField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at=models.DateTimeField(auto_now=True, null=True, blank=True)
    
    

def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits): 
    return ''.join(random.choice(chars) for _ in range(size)) 
  
def unique_vendor_code_generator(instance, new_vendor_code = None): 
    if new_vendor_code is not None: 
        vendor_code = slugify(new_vendor_code) 
    else: 
        vendor_code = slugify(instance.name) 
    Klass = instance.__class__ 
    qs_exists = Klass.objects.filter(vendor_code = vendor_code).exists() 
      
    if qs_exists: 
        new_vendor_code = "{vendor_code}-{randstr}".format( 
            vendor_code = vendor_code, randstr = random_string_generator(size = 4)) 
              
        return unique_vendor_code_generator(instance, new_vendor_code = new_vendor_code) 
    return vendor_code


def pre_save_receiver(sender, instance, *args, **kwargs): 
    if not instance.vendor_code: 
       instance.vendor_code = unique_vendor_code_generator(instance) 
pre_save.connect(pre_save_receiver, sender = Vendor) 