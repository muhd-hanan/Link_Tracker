from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

try:
    User.objects.create_superuser(
        username="admin",
        email="hananmuhdmkd@gmail.com",
        password="907255"
    )
    print("Superuser created")
except IntegrityError:
    print("Superuser already exists")
