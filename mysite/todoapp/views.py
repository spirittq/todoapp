from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, CategoryForm, TaskForm, TaskUpdateForm, TaskStatusForm, OrderingForm, StepForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from .models import Task, Category, Step
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.db import transaction
from django.contrib.auth.password_validation import MinimumLengthValidator, UserAttributeSimilarityValidator, NumericPasswordValidator, CommonPasswordValidator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def index(request):
    return render(request, 'index.html')


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"User profile updated")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        validators = [MinimumLengthValidator, NumericPasswordValidator, UserAttributeSimilarityValidator, CommonPasswordValidator]
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Email {email} already taken')
                    return redirect('register')
                else:
                    try:
                        validate_email(email)
                    except ValidationError as e:
                        messages.error(request, str(e))
                        return redirect('register')
                    try:
                        for validator in validators:
                            validator().validate(password1)
                    except ValidationError as e:
                        messages.error(request, str(e))
                        return redirect('register')
                    User.objects.create_user(username=username, email=email, password=password1)
                    new_user = authenticate(username=username, password=password1)
                    login(request, new_user)
                    return redirect('index')
        else:
            messages.error(request, "Passwords don't match!")
            return redirect('register')
    return render(request, 'register.html')


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks.html'
    paginate_by = 6

    def get_queryset(self):
        filter_val = self.request.GET.get('filter', None)
        if filter_val:
            return Task.objects.filter(user=self.request.user, category=filter_val).order_by('due_date')
        else:
            return Task.objects.filter(user=self.request.user).order_by('due_date')


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = "/todoapp/tasks"
    template_name = 'task_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(TaskCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TaskDetailView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    template_name = 'task.html'
    form_class = TaskStatusForm

    def get_success_url(self):
        return reverse_lazy('task', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    template_name = 'task_update.html'
    form_class = TaskUpdateForm

    def get_success_url(self):
        return reverse_lazy('task', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user

    def get_form_kwargs(self):
        kwargs = super(TaskUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = "/todoapp/tasks"
    template_name = 'task_delete.html'

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    success_url = '/todoapp/tasks/new'
    template_name = 'category_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['name', 'color']
    success_url = "/todoapp/tasks"
    template_name = 'category_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        category = self.get_object()
        return self.request.user == category.user


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    success_url = "/todoapp/tasks"
    template_name = 'category_delete.html'

    def test_func(self):
        category = self.get_object()
        return self.request.user == category.user


class StepCreateView(LoginRequiredMixin, CreateView):
    model = Step
    form_class = StepForm
    template_name = 'step_form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(StepCreateView, self).get_context_data(**kwargs)
        context['form'] = StepForm(initial={'task_id': self.kwargs['pk']})
        return context

    def get_success_url(self):
        return reverse_lazy('task', args=[str(self.kwargs['pk'])])


class StepDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Step
    template_name = 'step_delete.html'

    def test_func(self):
        step = self.get_object()
        return self.request.user == step.task_id.user

    def get_success_url(self):
        step = self.get_object()
        return reverse_lazy('task', args=[str(step.task_id.id)])


class StepListView(LoginRequiredMixin, ListView, FormView):
    model = Step
    template_name = "steps.html"
    form_class = OrderingForm

    def get_queryset(self):
        return Step.objects.filter(task_id_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(StepListView, self).get_context_data(**kwargs)
        context['task'] = self.kwargs['pk']
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            ordered_ids = form.cleaned_data["ordering"].split(',')
            with transaction.atomic():
                current_order = 1
                for lookup_id in ordered_ids:
                    group = Step.objects.get(lookup_id__exact=lookup_id)
                    group.number = current_order
                    group.save()
                    current_order += 1
        return redirect('task', self.kwargs['pk'])