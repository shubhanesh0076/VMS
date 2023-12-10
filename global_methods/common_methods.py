import uuid

class CommonGlobalMethods:
    def get_payload(
        self,
        status,
        body: dict = {},
        message: str = None,
        is_authenticated: bool = False,
        extra_information: dict = {},
    ):
        return {
            "is_authenticated": is_authenticated,
            "status": status,
            "message": message,
            "data": body,
            "extra_information": extra_information,
        }

    def is_authenticated_status(self, request):
        """
        check the authentication status...
        """
        try:
            if request.user.is_authenticated:
                return True
            return False

        except Exception as e:
            return False
    
    def generate_unique_po_number(self):
        prefix = "PO"
        unique_number = uuid.uuid4().int  # Get the integer value of the UUID
        po_number = f"{prefix}{unique_number}"
        return po_number
