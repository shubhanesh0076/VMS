from rest_framework.views import APIView
from vendor.models import Vendor
from .serializers import VendorAPISerializer
from global_methods.common_methods import CommonGlobalMethods as CGM
from global_methods.global_messages import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from typing import Any
from purchase_order.models import PerformanceMetrices, PurchaseOrderTracking
from purchase_order.api.serializers import PerformcnceMetrixSerializer
from django.db.models import F, Avg, ExpressionWrapper, fields
from datetime import datetime
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


_common_global_methods = CGM()


class VendorAPIVIEW(APIView):

    
    def __init__(self, **kwargs) -> None:
        self.venderserializer = VendorAPISerializer
        self.vendor_qs = Vendor.objects.all()
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        """
        Handle HTTP GET requests to retrieve information about vendors and list of vendors.

        ----------------
        Parameters:
            request (HttpRequest): The incoming HTTP request.
            args (tuple): Additional positional arguments.
            kwargs (dict): Additional keyword arguments.

        ----------------
        Returns:
            Response: A JSON response containing information about vendors.

        ----------------
        Raises:
            Http404: If a specific vendor is requested by vendor code, and it is not found.
            Exception: If an unexpected error occurs during the process.

        ----------------
        Usage:
            To retrieve details of a specific vendor:
                GET /api/vendor/?vendor-code=XYZ

            To retrieve a list of all vendors:
                GET /api/vendor/
        """
        data = request.GET
        vendor_code = data.get("vendor-code", None)

        try:
            if vendor_code is not None:
                try:
                    vendor_obj = self.vendor_qs.get(vendor_code=vendor_code)

                except Exception as e:
                    payload = _common_global_methods.get_payload(
                        status=status.HTTP_404_NOT_FOUND,
                        message=f"vendor {NOT_FOUND}",
                        is_authenticated=_common_global_methods.is_authenticated_status(
                            request
                        ),
                    )
                    return Response(payload, status=status.HTTP_404_NOT_FOUND)

                else:
                    serialized_vendor_obj = self.venderserializer(
                        vendor_obj, many=False
                    ).data
                    payload = _common_global_methods.get_payload(
                        status=status.HTTP_200_OK,
                        body=serialized_vendor_obj,
                        message=f"Vendor {DETAILS}",
                        is_authenticated=_common_global_methods.is_authenticated_status(
                            request
                        ),
                    )
                    return Response(payload, status=status.HTTP_200_OK)

            else:
                vendor_qs = self.vendor_qs.order_by("-created_at")
                serialized_vendor_data = self.venderserializer(
                    vendor_qs, many=True
                ).data

                payload = _common_global_methods.get_payload(
                    status=status.HTTP_200_OK,
                    body=serialized_vendor_data,
                    message=VENDOR_LIST,
                    is_authenticated=_common_global_methods.is_authenticated_status(
                        request
                    ),
                )
                return Response(payload, status=status.HTTP_200_OK)

        except Exception as e:
            payload = _common_global_methods.get_payload(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"An Error iccured: {e}",
                is_authenticated=_common_global_methods.is_authenticated_status(
                    request
                ),
            )
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        
        """
        Handle HTTP POST requests to create a new vendor.

        ----------------
        Parameters:
            request (HttpRequest): The incoming HTTP request.
            args (tuple): Additional positional arguments.
            kwargs (dict): Additional keyword arguments.

        ----------------
        Returns:
            Response: A JSON response indicating the result of the vendor creation.

        ----------------
        Raises:
            ValidationError: If the provided data fails validation.
            Exception: If an unexpected error occurs during the process.

        ----------------
        Usage:
            To create a new vendor, send a POST request to the endpoint with the vendor data in the request body.

        Example Request:
            POST /api/vendor/
            {
                "name": "kapil",
                "contact_details": "9057456774",
                "address": "faridabad, Haryana"
            }
            
        ---------------
        Example Response (Success):
            {
                "status": 201,
                "body": {
                    "vendor_info": {
                        "name": "kapil",
                        "contact_details": "9057456774",
                        "address": "faridabad, Haryana"
                        ...
                    }
                },
                "message": "Vendor created successfully.",
                "is_authenticated": true
            }

        ---------------
        Example Response (Validation Error):
            {
                "status": 400,
                "message": {
                    "field_name": ["Error message 1", "Error message 2", ...],
                    ...
                },
                "is_authenticated": true
            }

        ---------------
        Example Response (Internal Server Error):
            {
                "status": 500,
                "message": "An error occurred: Details of the error.",
                "is_authenticated": true
            }
        """
    
        try:
            serializer = self.venderserializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                payload = _common_global_methods.get_payload(
                    status=status.HTTP_201_CREATED,
                    body={"vendor_info": serializer.data},
                    message=VENDER_CREATED,
                    is_authenticated=_common_global_methods.is_authenticated_status(
                        request
                    ),
                )
                return Response(payload, status=status.HTTP_201_CREATED)

            payload = _common_global_methods.get_payload(
                status=status.HTTP_400_BAD_REQUEST,
                message=serializer.errors,
                is_authenticated=_common_global_methods.is_authenticated_status(
                    request
                ),
            )
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as ve:
            payload = _common_global_methods.get_payload(
                status=status.HTTP_400_BAD_REQUEST,
                message=ve,
                is_authenticated=_common_global_methods.is_authenticated_status(
                    request
                ),
            )
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            payload = _common_global_methods.get_payload(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"An error occurred: {str(e)}",
                is_authenticated=_common_global_methods.is_authenticated_status(
                    request
                ),
            )
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        
        """
        Handle HTTP PATCH requests to partially update information about a vendor.

        ---------------
        Parameters:
            request (HttpRequest): The incoming HTTP request.
            args (tuple): Additional positional arguments.
            kwargs (dict): Additional keyword arguments.

        ---------------
        Returns:
            Response: A JSON response indicating the result of the vendor update.

        ---------------
        Raises:
            Http400: If the 'vendor_code' is missing in the request data.
            Http404: If the vendor with the provided 'vendor_code' is not found.
            Exception: If an unexpected error occurs during the process.

        ---------------
        Usage:
            To partially update information about a vendor, send a PATCH request to the endpoint
            with the 'vendor_code' in the request data and the fields to be updated.

        ---------------
        Example Request:
            PATCH /api/vendor/
            {
                "vendor_code": "ABC",
                "updated_field": "New Value",
                ...
            }

        ---------------
        Example Response (Success):
            {
                "status": 202,
                "body": {
                    "updated_field": "New Value",
                    ...
                },
                "message": "Vendor information updated successfully.",
                "is_authenticated": true
            }

        ---------------
        Example Response (Validation Error):
            {
                "status": 400,
                "message": {
                    "field_name": ["Error message 1", "Error message 2", ...],
                    ...
                },
                "is_authenticated": true
            }

        ---------------
        Example Response (Vendor Not Found):
            {
                "status": 404,
                "message": "Vendor not found.",
                "is_authenticated": true
            }

        ---------------
        Example Response (Internal Server Error):
            {
                "status": 500,
                "message": "An error occurred: Details of the error.",
                "is_authenticated": true
            }
        """
        
        data = request.data
        vendor_code = data.get("vendor_code", None)

        if vendor_code is None:
            payload = _common_global_methods.get_payload(
                status=status.HTTP_400_BAD_REQUEST,
                message=VENDOR_CODE_NONE,
                is_authenticated=_common_global_methods.is_authenticated_status(
                    request
                ),
            )
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        try:
            vendor_obj = Vendor.objects.get(vendor_code=vendor_code)

        except ObjectDoesNotExist:
            payload = _common_global_methods.get_payload(
                status=status.HTTP_404_NOT_FOUND,
                message=f"Vendor {NOT_FOUND}",
                is_authenticated=_common_global_methods.is_authenticated_status(
                    request
                ),
            )
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            payload = _common_global_methods.get_payload(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"An error occured: {e}",
                is_authenticated=_common_global_methods.is_authenticated_status(
                    request
                ),
            )
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            serializer = self.venderserializer(
                instance=vendor_obj, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                data = serializer.data

                payload = _common_global_methods.get_payload(
                    status=status.HTTP_202_ACCEPTED,
                    body=data,
                    message=VENDOR_UPDATE,
                    is_authenticated=_common_global_methods.is_authenticated_status(
                        request
                    ),
                )
                return Response(payload, status=status.HTTP_202_ACCEPTED)
            payload = _common_global_methods.get_payload(
                status=status.HTTP_400_BAD_REQUEST,
                body=data,
                message=serializer.errors,
                is_authenticated=_common_global_methods.is_authenticated_status(
                    request
                ),
            )
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        
        """
        Handle HTTP DELETE requests to delete a vendor.

        ------------------
        Parameters:
            request (HttpRequest): The incoming HTTP request.

        ------------------
        Returns:
            Response: A JSON response indicating the result of the vendor deletion.

        ------------------
        Raises:
            Http404: If the 'vendor-code' is missing or the vendor with the provided code is not found.
            Exception: If an unexpected error occurs during the process.

        ------------------
        Usage:
            To delete a vendor, send a DELETE request to the endpoint with the 'vendor-code' in the query parameters.

        ------------------
        Example Request:
            DELETE /api/vendor/?vendor-code=ABC

        ------------------
        Example Response (Success):
            {
                "status": 200,
                "message": "Vendor deleted successfully.",
                "is_authenticated": true
            }

        ------------------
        Example Response (Vendor Not Found):
            {
                "status": 404,
                "message": "Vendor not found.",
                "is_authenticated": true
            }

        ------------------
        Example Response (Internal Server Error):
            {
                "status": 500,
                "message": "An error occurred: Details of the error.",
                "is_authenticated": true
            }
        """
        data = request.GET
        vendor_code = data.get("vendor-code", None)
        try:
            vendor_obj = self.vendor_qs.get(vendor_code=vendor_code)

        except ObjectDoesNotExist:
            payload = _common_global_methods.get_payload(
                status=status.HTTP_404_NOT_FOUND,
                message=NOT_FOUND,
                is_authenticated=_common_global_methods.is_authenticated_status(
                    request
                ),
            )
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            payload = _common_global_methods.get_payload(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"An error occured: {e}",
                is_authenticated=_common_global_methods.is_authenticated_status(
                    request
                ),
            )
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            vendor_obj.delete()
            payload = _common_global_methods.get_payload(
                status=status.HTTP_200_OK,
                message=DELETED,
                is_authenticated=_common_global_methods.is_authenticated_status(
                    request
                ),
            )
            return Response(payload, status=status.HTTP_200_OK)


class VendorPerformanceMetricesAPIView(APIView):
    
    """
    API view to retrieve and update performance metrics for a vendor.

    --------------
    Attributes:
        performance_metrix_serializer (Serializer): Serializer for performance metrics.
        performance_metrix_cls (QuerySet): QuerySet for PerformanceMetrices model.
        purchase_order_tracking_cls (QuerySet): QuerySet for PurchaseOrderTracking model.
        vendor_cls (QuerySet): QuerySet for Vendor model.

    --------------
    Methods:
        get_total_completed_po(vendor_id): Get the total completed purchase orders for a vendor.
        get_total_po(vendor_id): Get the total purchase orders for a vendor.
        get_on_time_delivery_rate(vendor_id): Calculate and get the on-time delivery rate for a vendor.
        get_quality_rating_average(vendor_id): Calculate and get the average quality rating for completed POs of a vendor.
        get_avg_response_time(vendor_id): Calculate and get the average response time for completed POs of a vendor.
        get_fullfillment_rate(vendor_id): Calculate and get the fulfillment rate for a vendor.
        get(request, vendor_id, *args, **kwargs): Handle HTTP GET requests to retrieve vendor performance metrics.
    
    """
    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the VendorPerformanceMetricesAPIView.
        
        --------------
        Args:
            kwargs: Additional keyword arguments.
        """
        self.performance_metrix_serializer = PerformcnceMetrixSerializer
        self.performance_metrix_cls = PerformanceMetrices.objects
        self.purchase_order_tracking_cls = PurchaseOrderTracking.objects
        self.vendor_cls = Vendor.objects
        super().__init__(**kwargs)

    def get_total_completed_po(self, vendor_id):
        """
        Get the total completed purchase orders for a vendor.

        ----------------
        Args:
            vendor_id (str): Vendor code.

        ----------------
        Returns:
            QuerySet: QuerySet of completed purchase orders.
        
        ----------------
        Raises:
            ObjectDoesNotExist: If the vendor with the provided 'vendor_id' is not found.
        """
        if not self.vendor_cls.filter(vendor_code=vendor_id).exists():
            raise ObjectDoesNotExist("Vendor not found")

        total_completed_po = self.purchase_order_tracking_cls.filter(
            vendor__vendor_code=vendor_id, status="completed"
        )
        return total_completed_po

    def get_total_po(self, vendor_id):
        """
        Get the total purchase orders for a vendor.

        ------------
        Args:
            vendor_id (str): Vendor code.

        ------------
        Returns:
            QuerySet: QuerySet of all purchase orders.
        
        ------------
        Raises:
            ObjectDoesNotExist: If the vendor with the provided 'vendor_id' is not found.
        """

        if not self.vendor_cls.filter(vendor_code=vendor_id).exists():
            raise ObjectDoesNotExist("Vendor not found")

        total_completed_po = self.purchase_order_tracking_cls.filter(
            vendor__vendor_code=vendor_id
        )
        return total_completed_po

    def get_on_time_delivery_rate(self, vendor_id):
        """
        Calculate and get the on-time delivery rate for a vendor.
        
        -----------
        Args:
            vendor_id (str): Vendor code.

        -----------
        Returns:
            float: On-time delivery rate.
        
        -----------
        Raises:
            ObjectDoesNotExist: If the vendor with the provided 'vendor_id' is not found.
        """
    
        total_completed_po = self.get_total_completed_po(vendor_id=vendor_id)
        completed_on_time_po = total_completed_po.filter(
            delivery_date__lte=F("on_time_delivery_date")
        )

        if total_completed_po.count() > 0:
            on_time_delivery_rate = round(
                (completed_on_time_po.count() / total_completed_po.count()) * 100, 2
            )
        else:
            on_time_delivery_rate = 0
        return on_time_delivery_rate

    def get_quality_rating_average(self, vendor_id):
        """
        Calculate and get the average quality rating for completed POs of a vendor.

        -------------
        Args:
            vendor_id (str): Vendor code.
            
        -------------
        Returns:
            float: Average quality rating.
        
        -------------
        Raises:
            ObjectDoesNotExist: If the vendor with the provided 'vendor_id' is not found.
        """
        total_completed_po = self.get_total_completed_po(vendor_id=vendor_id)

        if total_completed_po.count() > 0:
            avg_ratings = round(
                total_completed_po.aggregate(Avg("quality_rating")).get(
                    "quality_rating__avg", 0
                ),
                2,
            )
            return avg_ratings
        return 0

    def get_avg_response_time(self, vendor_id):
        """
        Calculate and get the average response time for completed POs of a vendor.

        -----------
        Args:
            vendor_id (str): Vendor code.

        -----------
        Returns:
            Duration: Average response time.
        
        -----------
        Raises:
            ObjectDoesNotExist: If the vendor with the provided 'vendor_id' is not found.
        """
        
        total_completed_po = self.get_total_completed_po(vendor_id=vendor_id)

        if total_completed_po.count() > 0:
            time_difference_expression = ExpressionWrapper(
                F("issue_date") - F("acknowledgment_date"),
                output_field=fields.DurationField(),
            )
            annotated_time_difference = total_completed_po.annotate(
                time_difference=time_difference_expression
            )
            average_response_time = annotated_time_difference.aggregate(
                Avg("time_difference")
            )["time_difference__avg"]
            return average_response_time
        return None

    def get_fullfillment_rate(self, vendor_id):
        """
        Calculate and get the fulfillment rate for a vendor.

        -------------
        Args:
            vendor_id (str): Vendor code.

        -------------
        Returns:
            float: Fulfillment rate.
        
        -------------
        Raises:
            ObjectDoesNotExist: If the vendor with the provided 'vendor_id' is not found.
        """
        total_completed_po = self.get_total_completed_po(vendor_id=vendor_id)
        total_po = self.get_total_po(vendor_id=vendor_id)

        if total_po.count() > 0:
            fullfillment_rate = (total_completed_po.count() / total_po.count()) * 100
            return fullfillment_rate
        return 0

    def get(self, request, vendor_id, *args, **kwargs):
        
        """
        Handle HTTP GET requests to retrieve vendor performance metrics.

        Args:
            request (HttpRequest): The incoming HTTP request.
            vendor_id (str): Vendor code.
            args (tuple): Additional positional arguments.
            kwargs (dict): Additional keyword arguments.

        Returns:
            Response: A JSON response containing vendor performance metrics.
        
        Raises:
            Http404: If the vendor with the provided 'vendor_id' is not found.
            Exception: If an unexpected error occurs during the process.
        """
        try:
            on_time_delivery_rate = self.get_on_time_delivery_rate(vendor_id=vendor_id)
            quality_average_ratings = self.get_quality_rating_average(
                vendor_id=vendor_id
            )
            avg_response_time = self.get_avg_response_time(vendor_id=vendor_id)
            fullfillment_rate = self.get_fullfillment_rate(vendor_id=vendor_id)

            try:
                vendor_instance = Vendor.objects.get(vendor_code=vendor_id)
                PerformanceMetrices.objects.update_or_create(
                    vendor=vendor_instance,
                    defaults={
                        'date':datetime.now(),
                        "on_time_delivery_rate": on_time_delivery_rate,
                        "quality_rating_avg": quality_average_ratings,
                        "average_response_time": avg_response_time,
                        "fulfillment_rate": fullfillment_rate
                    },
                )
                    
            except Exception as e:
                payload = _common_global_methods.get_payload(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message=f"Error occurse: {e}",
                    is_authenticated=_common_global_methods.is_authenticated_status(
                        request
                    ),
                )
                return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ObjectDoesNotExist:
            payload = _common_global_methods.get_payload(
                status=status.HTTP_404_NOT_FOUND,
                message=NOT_FOUND,
                is_authenticated=_common_global_methods.is_authenticated_status(
                    request
                ),
            )
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            payload = _common_global_methods.get_payload(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"An error occurse: {e}",
                is_authenticated=_common_global_methods.is_authenticated_status(
                    request
                ),
            )
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            vendor_performance_metrix = self.performance_metrix_cls.get(
                vendor=vendor_instance
            )
            serialized_performance_metrix_data = self.performance_metrix_serializer(
                vendor_performance_metrix, many=False
            ).data

            payload = _common_global_methods.get_payload(
                status=status.HTTP_200_OK,
                body=serialized_performance_metrix_data,
                message="Vendor Performance.",
                is_authenticated=_common_global_methods.is_authenticated_status(
                    request
                ),
            )
            return Response(payload, status=status.HTTP_200_OK)
