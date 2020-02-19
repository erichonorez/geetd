import uuid

from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator

class Todo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=False, blank=False, validators=[MinLengthValidator(1), MaxLengthValidator(255)])
    is_done = models.BooleanField(null=False, default=False)