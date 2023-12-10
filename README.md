# VMS

## Process of setup the project.
# 1:git clone the project.
  Ex: git clone "repo URL."
# 2: Create the virtualenv for project.
  Ex: virtualenv vene.
# 3: Activate the virtualenv.
  Ex: source venv/bin/activate.
# 4: Install the requirements.txt file.
   Ex: pip install -r requirements.txt
# 5: Apply the migrations.
  Ex: python3 manage.py makemigrations
      python3 manage.py migrate
      python3 manage.py createsuperuser

# 6: run the project:
    Ex: python3 manage.py runserver


# APIs Docs.

### 1: Get Vendor List
To retrieve a list of all vendors:
##### URL: http://127.0.0.1:8000/api/vendor/
##### Method: GET 
###### Ex: Response: {
    "is_authenticated": false,
    "status": 200,
    "message": "Vendor List",
    "data": [
        {
            "name": "kapilfedew",
            "contact_details": "9057456774",
            "vendor_code": "kapilfedew",
            "address": "faridabad, Haryana",
            "on_time_delivery_rate": null,
            "quality_rating_avg": null,
            "average_response_time": null,
            "fulfillment_rate": null,
            "created_at": "2023-12-05T18:12:46.223966Z",
            "updated_at": "2023-12-05T18:12:46.224051Z"
        },
        {
            "name": "Ajay Bhandary",
            "contact_details": "9983454323",
            "vendor_code": "ajay-bhandary",
            "address": "Noida , Up",
            "on_time_delivery_rate": null,
            "quality_rating_avg": null,
            "average_response_time": null,
            "fulfillment_rate": null,
            "created_at": "2023-12-05T17:37:40.559559Z",
            "updated_at": "2023-12-05T17:37:40.559605Z"
        }
    ],
    "extra_information": {}
}


### 2: Get Vendor Details
To retrieve a specific vendor details:
##### URL: http://127.0.0.1:8000/api/vendor/?vendor-code=kapil-4g21
##### Method: GET
###### Ex: Response: {
    "is_authenticated": false,
    "status": 200,
    "message": "Vendor Details",
    "data": {
        "name": "Vinay kumar",
        "contact_details": "8090657894",
        "vendor_code": "kapil-4g21",
        "address": "faridabad, Haryana",
        "on_time_delivery_rate": 34.78,
        "quality_rating_avg": null,
        "average_response_time": null,
        "fulfillment_rate": null,
        "created_at": "2023-12-05T18:15:20.452863Z",
        "updated_at": "2023-12-06T06:04:50.570981Z"
    },
    "extra_information": {}
}

### 3: Create Vendor Details
Create the vendor:
##### URL: http://127.0.0.1:8000/api/vendor/
##### Method: POST
###### Ex: Body: {
    "name": "kapil",
    "contact_details": "9057456774",
    "address": "faridabad, Haryana"
}
##### Response: {
    "is_authenticated": false,
    "status": 201,
    "message": "Vender has been successfully created.",
    "data": {
        "vendor_info": {
            "name": "Deep",
            "contact_details": "9057456774",
            "vendor_code": "deep",
            "address": "faridabad, Haryana",
            "on_time_delivery_rate": null,
            "quality_rating_avg": null,
            "average_response_time": null,
            "fulfillment_rate": null,
            "created_at": "2023-12-10T17:07:56.409662Z",
            "updated_at": "2023-12-10T17:07:56.409704Z"
        }
    },
    "extra_information": {}
}


### 4: Update Vendor Details
Update the vendor:
##### URL: http://127.0.0.1:8000/api/vendor/
##### Method: PATCH
###### Ex:{
    "name": "kapil",
    "contact_details": "9057456774",
    "address": "faridabad, Haryana"
}
##### Response: {
    "is_authenticated": false,
    "status": 201,
    "message": "Vender has been successfully Updated.",
    "data": {
        "vendor_info": {
            "name": "Deep",
            "contact_details": "9057456774",
            "vendor_code": "deep",
            "address": "faridabad, Haryana",
            "on_time_delivery_rate": null,
            "quality_rating_avg": null,
            "average_response_time": null,
            "fulfillment_rate": null,
            "created_at": "2023-12-10T17:07:56.409662Z",
            "updated_at": "2023-12-10T17:07:56.409704Z"
        }
    },
    "extra_information": {}
}


### 5: Delete Vendor
Delete the vendor:
##### URL: http://127.0.0.1:8000/api/vendor/?vendor-code=kapil-4g21
##### Method: DELETE
###### Ex Response: {
    "is_authenticated": false,
    "status": 200,
    "message": "vendor has been successfully deleted.",
    "data": {},
    "extra_information": {}
}


### 6: GET Vendor Performance Innformation.
Vendor performance: 
##### URL: http://127.0.0.1:8000/api/vendor/<vendor_code>/performance/
##### Method: GET
###### Ex:Response: {
    "is_authenticated": false,
    "status": 200,
    "message": "Vendor Performance.",
    "data": {
        "vendor": "shubham",
        "date": "2023-12-10T14:54:23.277530Z",
        "created_at": "2023-12-10T09:56:01.513570Z",
        "on_time_delivery_rate": 66.67,
        "quality_rating_avg": 7.33,
        "average_response_time": "01:51:17.826601",
        "fulfillment_rate": 60.0
    },
    "extra_information": {}
}


### 7: Product Order List
Product Order List:
##### URL: http://127.0.0.1:8000/api/purchase-orders/
##### Method: GET
###### Ex: Response:{
    "is_authenticated": false,
    "status": 200,
    "message": "Producted Order Track List.",
    "data": [
        {
            "po_number": "PO288806588519884503844868458358346557262",
            "vendor": "kapilfedew",
            "order_date": "2023-12-06T18:26:40.834813Z",
            "delivery_date": null,
            "on_time_delivery_date": null,
            "items": {
                "vegitables": [
                    "Chilly",
                    "Carrot"
                ],
                "electronics_item": [
                    "computer",
                    "mouse",
                    "keyword"
                ]
            },
            "quantity": 10,
            "status": "canceled",
            "quality_rating": 7.0,
            "issue_date": null,
            "acknowledgment_date": null
        },
        {
            "po_number": "PO213677533588261468457307031548399725343",
            "vendor": "shubham",
            "order_date": "2023-12-08T11:15:13.761258Z",
            "delivery_date": "2023-12-09T14:33:13.761258Z",
            "on_time_delivery_date": "2023-12-09T14:33:13.761258Z",
            "items": {
                "vegitables": [
                    "Chilly",
                    "Carrot"
                ],
                "electronics_item": [
                    "computer",
                    "mouse",
                    "keyword"
                ]
            },
            "quantity": 6,
            "status": "completed",
            "quality_rating": 7.0,
            "issue_date": "2023-12-09T14:31:13.761258Z",
            "acknowledgment_date": "2023-12-09T08:59:20.281455Z"
        },
    ],
    "extra_information": {}
}

### 8: Specific Product Order Details
Specific Product Order Details:
##### URL: [http://127.0.0.1:8000/api/purchase-orders/](http://127.0.0.1:8000/api/purchase-orders/?po-number=PO316433673163031889464686993295049691891)
##### Method: GET
###### Ex: Response:{
    "is_authenticated": false,
    "status": 200,
    "message": "Product Details.",
    "data": {
        "po_number": "PO316433673163031889464686993295049691891",
        "vendor": "shubham",
        "order_date": "2023-12-08T11:21:26.196016Z",
        "delivery_date": null,
        "items": {
            "vegitables": [
                "Chilly",
                "Carrot"
            ],
            "electronics_item": [
                "computer",
                "mouse",
                "keyword"
            ]
        },
        "quantity": 50,
        "status": "pending",
        "quality_rating": 5.0,
        "issue_date": null,
        "acknowledgment_date": "2023-12-09T09:43:52.128501Z"
    },
    "extra_information": {}
}


### 9: Create Product Order Details
Specific Product Order Details:
##### URL: http://127.0.0.1:8000/api/purchase-orders/
##### Method: POST
###### Ex: BODY: {
    "vendor_code":"shubham",
    "po_id": "PO331195806869265469920819167642994109593"
} 
###### Response:{
    "is_authenticated": false,
    "status": 200,
    "message": "Product Details.",
    "data": {
        "po_number": "PO316433673163031889464686993295049691891",
        "vendor": "shubham",
        "order_date": "2023-12-08T11:21:26.196016Z",
        "delivery_date": null,
        "items": {
            "vegitables": [
                "Chilly",
                "Carrot"
            ],
            "electronics_item": [
                "computer",
                "mouse",
                "keyword"
            ]
        },
        "quantity": 50,
        "status": "pending",
        "quality_rating": 5.0,
        "issue_date": null,
        "acknowledgment_date": "2023-12-09T09:43:52.128501Z"
    },
    "extra_information": {}
}

### 10: Create Product Order Details
Update Product Order Details:
##### URL: http://127.0.0.1:8000/api/purchase-orders/
##### Method: PATCH
###### Ex: BODY: {
    "vendor_code": "shubham",
    "delivery_date": "2023-12-10 06:56:41.571828",
    "po_number": "PO331195806869265469920819167642994109593",
    "status": "completed",
    "on_time_delivery_date": "2023-12-10 08:56:41.571828"
}
###### Response:{
    "is_authenticated": false,
    "status": 202,
    "message": "Product order track has been successfully updated.",
    "data": {
        "po_number": "PO331195806869265469920819167642994109593",
        "vendor": "shubham",
        "order_date": "2023-12-10T05:53:13.612304Z",
        "delivery_date": "2023-12-10T06:56:41.571828Z",
        "on_time_delivery_date": "2023-12-10T08:56:41.571828Z",
        "items": {
            "vegitables": [
                "Chilly",
                "Carrot"
            ],
            "electronics_item": [
                "computer",
                "mouse",
                "keyword"
            ]
        },
        "quantity": 30,
        "status": "completed",
        "quality_rating": 8.0,
        "issue_date": "2023-12-10T05:56:41.571828Z",
        "acknowledgment_date": "2023-12-10T05:55:41.571828Z"
    },
    "extra_information": {}
}


### 11: Create Product Order Details
Delete Product Order Details:
##### URL: http://127.0.0.1:8000/api/purchase-orders/?po-number=PO12947992029633862152382849040421254434
##### Method: DELETE
###### Ex: Response:{
    "is_authenticated": false,
    "status": 200,
    "message": "Product order track has been deleted.",
    "data": {},
    "extra_information": {}
}


### 12: Create Product Order Details
API view to handle the acknowledgment of product delivery by a vendor for a specific purchase order.

##### URL: http://127.0.0.1:8000/api/purchase-orders/PO331195806869265469920819167642994109593/acknowledge/
##### Method: POST
###### Ex: BODY: {
    "vendor_code":"shubham",
    "po_id": "PO331195806869265469920819167642994109593"
}
###### Response:{
    "is_authenticated": false,
    "status": 200,
    "message": "Vendor acknowledged product successfully.",
    "data": {},
    "extra_information": {}
}
