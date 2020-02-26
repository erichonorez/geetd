from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View
from django.urls import reverse

from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator

from ..models import Todo
from ..models import INBOX


def get_sidebar_context():
    return {'states': Todo.STATES}


class HomeView(View):

    def get(self, request):
        state = request.GET.get('state', INBOX)
        todos = Todo.objects \
            .filter(state=state) \
            .order_by('priority_order')
        response = render(request, 'todo/index.html',
                          {'todos': todos, 'selected_state': state, 'sidebar': get_sidebar_context()})
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
                'sidebar': get_sidebar_context(),
                'selected_state': selected_state,
                'toggleCompleteForm': form
            })
            return response

        todo = get_object_or_404(Todo, pk=form.cleaned_data['todo_id'])
        todo.is_done = not todo.is_done
        todo.save()

        return HttpResponseRedirect(reverse('web-todo-list') + '?state=' + selected_state)


class AddTodoForm(forms.Form):
    title = forms.CharField(required=True, label='Title*', validators=[MinLengthValidator(1), MaxLengthValidator(255)])
    state = forms.ChoiceField(required=True, label='State*', choices=Todo.STATES)
    referrer = forms.URLField(required=True)


class AddTodoView(View):

    def get(self, request):
        form = AddTodoForm(initial={'referrer':request.META.get('HTTP_REFERER', reverse('web-todo-list'))})
        return render(request, 'todo/add.html', {'form': form, 'sidebar': get_sidebar_context()})


class CreateTodoView(View):

    def post(self, request):
        form = AddTodoForm(request.POST)
        if not form.is_valid():
            return render(request, 'todo/add.html', {'form': form, 'sidebar': get_sidebar_context()})

        todo = Todo(title=form.cleaned_data['title'], state=form.cleaned_data['state'])
        todo.save()

        return HttpResponseRedirect(form.cleaned_data['referrer'])
