import uuid

from django.db import models
from django.db.models import Q

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
    priority_order = models.IntegerField(default=0)

    def move_to_state(self, state):
        self.priority_order = Todo.get_next_priority_order(state)
        self.state = state
        self.save()
    
    def prioritize(self, priority_order):
        #TODO: replace with one update query
        todos = Todo.objects.filter(
            ~Q(pk=self.id),
            Q(state=self.state),
            Q(priority_order__gte=priority_order),
            Q(priority_order__lt=self.priority_order)
        ).order_by('priority_order')
        
        for idx, todo in enumerate(todos, start=1):
            todo.priority_order += idx
            todo.save()

        self.priority_order = priority_order
        self.save()

    def save(self, *args, **kwargs):
        if self._state.adding:
            try:
                self.priority_order = Todo.get_next_priority_order(self.state)
            except:
                pass

        super(Todo, self).save(*args, **kwargs)

    @staticmethod
    def get_next_priority_order(state):
        return Todo.objects.filter(state=state).order_by('-priority_order').first().priority_order + 1