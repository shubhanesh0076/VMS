from typing import Any
from .serializers import PurchaseOrderSerializer, PerformcnceMetrixSerializer
from rest_framework.views import APIView
from ..models import PurchaseOrderTracking, PerformanceMetrices
from rest_framework.response import Response
from global_methods.global_messages import *
from global_methods.common_methods import CommonGlobalMethods as CGM
from rest_framework import status
from rest_framework.validators import ValidationError
from vendor.models import Vendor
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

_cgm = CGM()


class PurchaseOrderTrackAPIView(APIView):
    """
    API view to retrieve, create, update, or delete purchase order tracking information.

    --------------
    Attributes:
        productordertrack_serializer: Serializer class for Purchase Order objects.
        product_order_track_qs: QuerySet for Purchase Order Tracking objects.

    --------------
    Methods:
        get(self, request, *args, **kwargs): Retrieve a list of purchase order tracking information
        or details of a specific purchase order.
        post(self, request, *args, **kwargs): Create a new purchase order tracking entry.
        patch(self, request, *args, **kwargs): Update details of an existing purchase order tracking entry.
        delete(self, request): Delete a specific purchase order tracking entry.
    """
    
    def __init__(self, **kwargs: Any) -> None:
        self.productordertrack_serializer = PurchaseOrderSerializer
        self.product_order_track_qs = PurchaseOrderTracking.objects.all()
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        data = request.GET
        po_number = data.get("po-number", None)
        filter_by_vendor = data.get("vendor-name", None)

        try:
            if po_number is None:
                if filter_by_vendor is not None:
                    filtered_purchased_order_qs = self.product_order_track_qs.filter(
                        vendor__name=filter_by_vendor
                    )
                    serialized_purchased_order = self.productordertrack_serializer(
                        filtered_purchased_order_qs, many=True
                    ).data

                else:
                    serialized_purchased_order = self.productordertrack_serializer(
                        self.product_order_track_qs, many=True
                    ).data

                payload = _cgm.get_payload(
                    status=status.HTTP_200_OK,
                    body=serialized_purchased_order,
                    message=PRODUCT_ORDER_TRACK_LIST,
                    is_authenticated=_cgm.is_authenticated_status(request),
                )
                return Response(payload, status=status.HTTP_200_OK)

            else:
                try:
                    product_order_track_obj = self.product_order_track_qs.get(
                        po_number=po_number
                    )

                except ObjectDoesNotExist:
                    payload = _cgm.get_payload(
                        status=status.HTTP_404_NOT_FOUND,
                        message=NOT_FOUND,
                        is_authenticated=_cgm.is_authenticated_status(request),
                    )
                    return Response(payload, status=status.HTTP_404_NOT_FOUND)

                except Exception as e:
                    payload = _cgm.get_payload(
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        message=f"An error occurse: {e}.",
                        is_authenticated=_cgm.is_authenticated_status(request),
                    )
                    return Response(
                        payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                else:
                    serialized_product_order_track = self.productordertrack_serializer(
                        product_order_track_obj, many=False
                    ).data

                    payload = _cgm.get_payload(
                        status=status.HTTP_200_OK,
                        body=serialized_product_order_track,
                        message=f"Product Details.",
                        is_authenticated=_cgm.is_authenticated_status(request),
                    )
                    return Response(payload, status=status.HTTP_200_OK)

        except Exception as e:
            payload = _cgm.get_payload(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"An error occurred: {str(e)}",
                is_authenticated=_cgm.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = self.productordertrack_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                try:
                    vendor = Vendor.objects.get(vendor_code=data.get("vendor_code"))
                except Exception as e:
                    payload = _cgm.get_payload(
                        status=status.HTTP_404_NOT_FOUND,
                        message="Vendor Not Found",
                        is_authenticated=_cgm.is_authenticated_status(request),
                    )
                    return Response(payload, status=status.HTTP_404_NOT_FOUND)
                else:
                    serializer.save(vendor=vendor)
                    payload = _cgm.get_payload(
                        status=status.HTTP_201_CREATED,
                        body=serializer.data,
                        message=PRODUCT_ORDER_TRACK_CREATE,
                        is_authenticated=_cgm.is_authenticated_status(request),
                    )
                    return Response(payload, status=status.HTTP_201_CREATED)

            payload = _cgm.get_payload(
                status=status.HTTP_400_BAD_REQUEST,
                message=serializer.errors,
                is_authenticated=_cgm.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as ve:
            payload = _cgm.get_payload(
                status=status.HTTP_400_BAD_REQUEST,
                message=ve,
                is_authenticated=_cgm.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            payload = _cgm.get_payload(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"An error occurred: {str(e)}",
                is_authenticated=_cgm.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        data = request.data
        po_number = data.get("po_number", None)

        if po_number is None:
            payload = _cgm.get_payload(
                status=status.HTTP_400_BAD_REQUEST,
                message=PRODUCT_ORDER_TRACK_NONE,
                is_authenticated=_cgm.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        try:
            purchase_order_obj = PurchaseOrderTracking.objects.get(po_number=po_number)

        except ObjectDoesNotExist:
            payload = _cgm.get_payload(
                status=status.HTTP_404_NOT_FOUND,
                message=f"Purchase order {NOT_FOUND}",
                is_authenticated=_cgm.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            payload = _cgm.get_payload(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"An error occured: {e}",
                is_authenticated=_cgm.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            serializer = self.productordertrack_serializer(
                instance=purchase_order_obj, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                data = serializer.data

                payload = _cgm.get_payload(
                    status=status.HTTP_202_ACCEPTED,
                    body=data,
                    message=PRODUCT_ORDER_TRACK_UPDATE,
                    is_authenticated=_cgm.is_authenticated_status(request),
                )
                return Response(payload, status=status.HTTP_202_ACCEPTED)
            payload = _cgm.get_payload(
                status=status.HTTP_400_BAD_REQUEST,
                body=data,
                message=serializer.errors,
                is_authenticated=_cgm.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = request.GET
        po_number = data.get("po-number", None)
        try:
            po_obj = self.product_order_track_qs.get(po_number=po_number)

        except ObjectDoesNotExist:
            payload = _cgm.get_payload(
                status=status.HTTP_404_NOT_FOUND,
                message=NOT_FOUND,
                is_authenticated=_cgm.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            payload = _cgm.get_payload(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"An error occured: {e}",
                is_authenticated=_cgm.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            po_obj.delete()
            payload = _cgm.get_payload(
                status=status.HTTP_200_OK,
                message=PRODUCT_ORDER_TRACK_DELETE,
                is_authenticated=_cgm.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_200_OK)


class VendorPerformanceMetricesAcknowledgementAPIView(APIView):
    """
    API view to handle the acknowledgment of product delivery by a vendor for a specific purchase order.

    --------------
    Attributes:
        performance_metrix_serializer: Serializer class for Performance Metrics objects.
        performance_metrix_cls: Model class for Performance Metrics objects.
        purchase_order_tracking_cls: Model class for Purchase Order Tracking objects.
        vendor_cls: Model class for Vendor objects.

    --------------
    Methods:
        post(self, request, po_id, *args, **kwargs): Acknowledge the delivery of products for a specific
        purchase order by updating the acknowledgment date in the Purchase Order Tracking object.
    """
    def __init__(self, **kwargs: Any) -> None:
        self.performance_metrix_serializer = PerformcnceMetrixSerializer
        self.performance_metrix_cls = PerformanceMetrices.objects
        self.purchase_order_tracking_cls = PurchaseOrderTracking.objects
        
        self.vendor_cls = Vendor.objects
        super().__init__(**kwargs)
    
    def post(self, request, po_id, *args, **kwargs):
        po_id = request.data.get('po_id')
        
        if po_id is None:
            payload = _cgm.get_payload(
                status=status.HTTP_400_BAD_REQUEST,
                body={},
                message="PO ID can not be None.",
                is_authenticated=_cgm.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
            po_obj = self.purchase_order_tracking_cls.get(po_number=po_id) 
            po_obj.acknowledgment_date=datetime.now()
            po_obj.save()
            
        except ObjectDoesNotExist:
            payload = _cgm.get_payload(
                status=status.HTTP_404_NOT_FOUND,
                body={},
                message="PO Not Found.",
                is_authenticated=_cgm.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_404_NOT_FOUND)
        
        
        payload = _cgm.get_payload(
                status=status.HTTP_200_OK,
                body={},
                message="Vendor acknowledged product successfully.",
                is_authenticated=_cgm.is_authenticated_status(request),
        )
        return Response(payload, status=status.HTTP_200_OK)
