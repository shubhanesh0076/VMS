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

### Get Vendor List
##### URL: http://127.0.0.1:8000/api/vendor/
###### Ex: {
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
