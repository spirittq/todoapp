from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, CategoryForm, TaskForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from .models import Task, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView


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
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Email {email} already taken')
                    return redirect('register')
                else:
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


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    success_url = '/todoapp/tasks/new'
    template_name = 'category_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)