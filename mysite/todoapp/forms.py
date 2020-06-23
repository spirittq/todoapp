from .models import Profile, Category, Task
from django import forms
from django.contrib.auth.models import User
from colorfield.widgets import ColorWidget




class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['pic']


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'due_date', 'importance']
        widgets = {'description': forms.Textarea(attrs={'style':'resize:none; height: 100px;'}),
                   'due_date': forms.DateInput(attrs={'class':'datepicker'})}


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)


class CategoryForm(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = Category
        fields = ['name', 'color']
        widgets = {'color': ColorWidget}