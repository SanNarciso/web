from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _


from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True,
    )

    email_verify = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Video(models.Model):
    title = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    file = models.ImageField(default='')
    image = models.ImageField(default='')

    create_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария', blank=True, null=True)
    question = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name='Вопрос', blank=True, null=True, related_name='comments_video')
    text = models.TextField(verbose_name='')
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Task(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор вопроса', blank=True, null=True)
    title = models.CharField('Название', max_length=50)
    task = models.TextField('Описание')
    create_date = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.title


class CommentTask(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария', blank=True, null=True)
    question = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Вопрос', blank=True, null=True, related_name='comments_task')
    text = models.TextField(verbose_name='')
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
