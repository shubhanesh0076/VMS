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
