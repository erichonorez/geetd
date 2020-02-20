import uuid

from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator

from django.core.exceptions import ValidationError

INBOX = 'inbox'
NEXT = 'next'

class ValidateOnSaveMixin():
    def save(self, skip_validate=False, **kwargs):
        if not skip_validate:
            self.full_clean()
        super(ValidateOnSaveMixin, self).save(kwargs)

class Todo(ValidateOnSaveMixin, models.Model):
    STATES = (
        (INBOX, 'Inbox'),
        (NEXT, 'Next')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=False, blank=False, validators=[MinLengthValidator(1), MaxLengthValidator(255)])
    is_done = models.BooleanField(null=False, default=False)
    state = models.CharField(max_length=5, choices=STATES, default=INBOX)