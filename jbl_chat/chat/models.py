from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# conversation
  # id
  # users: guid[]

# message
  # id
  # timestamp
  # content