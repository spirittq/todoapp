from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from colorfield.fields import ColorField
from datetime import date
import uuid


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

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        blank=True,
        default='o',
        help_text='Status of the task',
    )

    IMPORTANCE = (
        ('l', 'low'),
        ('m', 'medium'),
        ('h', 'high')
    )

    importance = models.CharField(
        max_length=1,
        choices=IMPORTANCE,
        blank=True,
        default='m',
        help_text='Importance of the task',
    )

    @property
    def is_overdue(self):
        if self.due_date and date.today() > self.due_date:
            return True
        return False

    def get_absolute_url(self):
        return reverse('task', args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


class Step(models.Model):

    title = models.CharField('Title', max_length=200, help_text="Step name")
    description = models.TextField('Description', max_length=1000, help_text='Step description')
    due_date = models.DateField('Deadline', null=True, blank=True, help_text='Step deadline')
    task_id = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True, related_name='steps')
    lookup_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Step'
        verbose_name_plural = 'Steps'
        ordering = ['number']

    def order():
        default_number = 0
        return default_number

    number = models.IntegerField('Step number', default=order)


class Category(models.Model):
    name = models.CharField('Name', max_length=200, help_text="Category name")
    color = ColorField(default='#E57373')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='category')

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

    def crop_center(self, pil_img, crop_width, crop_height):
        img_width, img_height = pil_img.size
        return pil_img.crop(((img_width - crop_width) // 2,
                             (img_height - crop_height) // 2,
                             (img_width + crop_width) // 2,
                             (img_height + crop_height) // 2))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        img = Image.open(self.pic.path)
        output_size = (300, 300)
        img = self.crop_center(img, min(img.size), min(img.size))
        img.thumbnail(output_size)
        img.save(self.pic.path)

