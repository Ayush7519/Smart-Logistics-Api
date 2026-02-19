from django.db import models
from .base import BaseModel


# -----------------------------------------------------------------------------------------------
# this is the testing model.
# -----------------------------------------------------------------------------------------------
class TestModel(BaseModel):
    name = models.CharField(max_length=50)
