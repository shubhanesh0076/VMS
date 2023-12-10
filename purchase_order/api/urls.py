from django.urls import path, include
from .views import PurchaseOrderTrackAPIView, VendorPerformanceMetricesAcknowledgementAPIView
app_name="purchase_orders"

urlpatterns = [
    path('', PurchaseOrderTrackAPIView.as_view(), name="purchase_order"),
    path('<str:po_id>/acknowledge/', VendorPerformanceMetricesAcknowledgementAPIView.as_view(), name="acknowledgement"),
]

