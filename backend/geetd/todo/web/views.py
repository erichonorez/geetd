from django.shortcuts import render
from django.views import View

from ..models import Todo
from ..models import INBOX


class HomeView(View):

    def get(self, request):
        state = request.GET.get('state', INBOX)
        todos = Todo.objects\
                    .filter(state=state)\
                    .order_by('priority_order')
        return render(request, 'todo/index.html', {
            'todos': todos,
            'states': Todo.STATES,
            'selected_state': state,
        })
