from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Task(models.Model):
    title = models.CharField('Pavadinimas', max_length=200, help_text="Task name")
    description = models.TextField('Aprašymas', max_length=1000, help_text='Task description')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='tasks')
    date_created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField('Deadline', null=True, blank=True, help_text='Task deadline')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    STATUS = (
        ('o', 'ongoing'),
        ('f', 'finished'),
        ('p', 'paused'),
        ('a', 'abandoned'),
    )

    IMPORTANCE = (
        ('l', 'low'),
        ('m', 'medium'),
        ('h', 'high')
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


class Step(models.Model):
    title = models.CharField('Pavadinimas', max_length=200, help_text="Step name")
    description = models.TextField('Aprašymas', max_length=1000, help_text='Step description')
    due_date = models.DateField('Deadline', null=True, blank=True, help_text='Step deadline')
    task_id = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True, related_name='steps')
    number = models.IntegerField('Step number')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Step'
        verbose_name_plural = 'Steps'


class Category(models.Model):
    name = models.CharField('Pavadinimas', max_length=200, help_text="Category name")
    color = models.CharField('Color code', default='ffffff', max_length=200, help_text="Color code")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.ImageField(default="default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profile"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        img = Image.open(self.pic.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.pic.path)

