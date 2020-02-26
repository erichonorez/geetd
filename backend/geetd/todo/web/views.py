from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View
from django.urls import reverse

from ..models import Todo
from ..models import INBOX


class HomeView(View):

    def get(self, request):
        state = request.GET.get('state', INBOX)
        todos = Todo.objects\
                    .filter(state=state)\
                    .order_by('priority_order')
        response = render(request, 'todo/index.html', {'todos': todos, 'states': Todo.STATES, 'selected_state': state, })
        response.set_cookie('selected_state', state, httponly=True)
        return response


class ToggleCompleteForm(forms.Form):
    todo_id = forms.UUIDField(required=True)


class ToggleCompleteView(View):

    def post(self, request):
        form = ToggleCompleteForm(request.POST)
        selected_state = request.COOKIES.get('selected_state', INBOX)
        if not form.is_valid():
            todos = Todo.objects \
                .filter(state=selected_state) \
                .order_by('priority_order')
            response = render(request, 'todo/index.html', {
                'todos': todos,
                'states': Todo.STATES,
                'selected_state': selected_state,
                'toggleCompleteForm': form
            })
            return response

        todo = get_object_or_404(Todo, pk=form.cleaned_data['todo_id'])
        todo.is_done = not todo.is_done
        todo.save()

        return HttpResponseRedirect(reverse('web-todo-list') + '?state=' + selected_state)