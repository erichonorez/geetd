from django import forms
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View
from django.urls import reverse

from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator

from rest_framework import serializers

from ..api.serializers import TodoSerializer
from ..models import Todo
from ..models import INBOX


def get_sidebar_context():
    return {'states': Todo.STATES}


class HomeView(View):

    def get(self, request):
        state = request.GET.get('state', INBOX)
        todos = Todo.objects.get_by_state(state)
        return render(request, 'todo/index.html',
                      {'todos': todos, 'selected_state': state, 'sidebar': get_sidebar_context()})


class ToggleCompleteView(View):

    def post(self, request, todo_id):
        todo = get_object_or_404(Todo, pk=todo_id)
        todo.is_done = not todo.is_done
        todo.save()

        todo_serializer = TodoSerializer(todo)
        return JsonResponse(todo_serializer.data)


class WithReferrer(forms.Form):
    referrer = forms.URLField(required=True)


class TodoForm(WithReferrer, forms.Form):
    title = forms.CharField(required=True, label='Title*', validators=[MinLengthValidator(1), MaxLengthValidator(255)])
    state = forms.ChoiceField(required=True, label='State*', choices=Todo.STATES)


class CreateTodoView(View):

    def get(self, request):
        form = TodoForm(initial={'referrer': request.META.get('HTTP_REFERER', reverse('web-todo-list'))})
        return render(request, 'todo/add.html', {'form': form, 'sidebar': get_sidebar_context()})

    def post(self, request):
        form = TodoForm(request.POST)
        if not form.is_valid():
            return render(request, 'todo/add.html', {'form': form, 'sidebar': get_sidebar_context()})

        todo = Todo(title=form.cleaned_data['title'], state=form.cleaned_data['state'])
        todo.save()

        return HttpResponseRedirect(form.cleaned_data['referrer'])


class DetailTodoView(View):

    def get(self, request, todo_id):
        todo = get_object_or_404(Todo, pk=todo_id)
        form_data = todo.__dict__
        form_data['referrer'] = request.META.get('HTTP_REFERER', reverse('web-todo-list'))
        form = TodoForm(data=form_data)
        return render(request, 'todo/show.html', {'todo': todo, 'form': form, 'sidebar': get_sidebar_context()})

    def post(self, request, todo_id):
        todo = get_object_or_404(Todo, pk=todo_id)
        form = TodoForm(request.POST)
        if not form.is_valid():
            return render(request, 'todo/show.html', {'todo': todo, 'form': form, 'sidebar': get_sidebar_context()})

        todo.title = form.cleaned_data['title']
        todo.state = form.cleaned_data['state']
        todo.save()

        return HttpResponseRedirect(form.cleaned_data['referrer'])


class DeleteTodoView(View):

    def post(self, request, todo_id):
        todo = get_object_or_404(Todo, pk=todo_id)
        todo.delete()

        form = WithReferrer(request.POST)
        if not form.is_valid():
            redirect_url = reverse('web-todo-list')
        else:
            redirect_url = form.cleaned_data['referrer']

        # TODO: redirect to the list of todo in the same state
        return HttpResponseRedirect(redirect_url)


class PriorityzeTodoSerializer(serializers.Serializer):
    priority_order = serializers.IntegerField(min_value=0)


class PrioritizeTodoView(View):

    def post(self, request, todo_id):
        serializer = PriorityzeTodoSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        todo = get_object_or_404(Todo, pk=todo_id)
        todo.prioritize(serializer.validated_data['priority_order'])
        todo_serializer = TodoSerializer(todo)
        return JsonResponse(todo_serializer.data)


class ArchiveTodoInStateForm(forms.Form):
    state = forms.CharField(required=True)


class ArchiveTodosInStateView(View):

    def post(self, request):
        form = ArchiveTodoInStateForm(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('web-todo-list')))

        todos = Todo.objects.get_by_state(form.cleaned_data['state'])
        for todo in todos:
            if todo.is_done:
                todo.is_archived = True
                todo.save()

        todos = Todo.objects.get_by_state(form.cleaned_data['state'])
        for idx, todo in enumerate(todos, start=0):
            todo.priority_order = idx
            todo.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('web-todo-list')))


class ArchivedTodosView(View):

    def get(self, request):
        todos = Todo.archived.all()
        return render(request, 'todo/archived.html', context={'todos': todos, 'sidebar': get_sidebar_context(), 'archived_selected': True})


class ArchiveTodoView(View):

    def post(self, request, todo_id):
        todo = get_object_or_404(Todo, pk=todo_id)
        todo.is_archived = True
        todo.save()

        todos = Todo.objects.get_by_state(todo.state)
        for idx, t in enumerate(todos, start=0):
            t.priority_order = idx
            t.save()

        return HttpResponseRedirect(reverse('web-todo-list') + '?state=' + todo.state)