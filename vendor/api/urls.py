from django.urls import path, include
from .views import VendorAPIVIEW, VendorPerformanceMetricesAPIView
app_name="vendors"

urlpatterns = [
    path('', VendorAPIVIEW.as_view(), name="vendor"),
    path('<str:vendor_id>/performance/', VendorPerformanceMetricesAPIView.as_view(), name="performance-metrix")
]

