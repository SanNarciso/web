from django.shortcuts import render
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin, CreateView

from .forms import UserCreationForm, CommentForm, TaskForm, CommentFormTask, AuthenticationForm
from .models import Video, Task
from .get_video import open_file


from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator as \
    token_generator

from django.contrib import messages

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from .utils import send_email_for_verify

from .models import Video


User = get_user_model()


def task_list(request):
    tasks = Task.objects.all()
    context = {'tasks': tasks}
    return render(request, 'home.html', context)


def view_geo(request):
    return render(request, 'geogebra/geogebra.html')


def view_profile(request):
    return render(request, 'profile.html')


def video_list(request):
    videos = Video.objects.all().order_by('-id')
    context = {'videos': videos}
    return render(request, 'videos/video_list.html', context)


def create_video(request):
    if request.method == "POST":
        if "file" in request.FILES:
            file2 = request.FILES["file"]
        else:
            file2 = ' '
        if "image" in request.FILES:
            image2 = request.FILES["image"]
        else:
            image2 = ' '

        if "title" in request.POST:
            title2 = request.POST["title"]
        else:
            title2 = ''
        description2 = request.POST["description"]

        file_format_check = str(file2).split('.')[-1].strip()
        image_format_check = str(image2).split('.')[-1].strip()

        if title2 == '':
            messages.error(request, 'Некорректный заголовок')
        elif file2 == ' ':
            messages.error(request, 'Некорректный файл изображения')
        elif image2 == ' ':
            messages.error(request, 'Некорректный файл изображения для значка')
        elif file_format_check != "png"\
                and file_format_check != "jpg" \
                and file_format_check != "bmp" \
                and file_format_check != "jpeg":
            messages.error(request, 'Некорректный формат изображения задачи (png, jpg, jpeg, bmp)')
        elif image_format_check != "png"\
                and image_format_check != "jpg"\
                and image_format_check != "bmp"\
                and image_format_check != "jpeg":
            messages.error(request, 'Некорректный формат изображения значок (png, jpg, jpeg, bmp)')
        else:
            document = Video.objects.create(file=file2, image=image2, title=title2, description=description2)
            document.save()
            return redirect('video_list')
    return render(request, 'videos/create_video.html')


class video_detail(FormMixin, DetailView):
    model = Video
    template_name = 'videos/video_detail.html'
    context_object_name = 'video'
    form_class = CommentForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('video_detail', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.question = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class Create(CreateView):
    model = Task
    template_name = 'create_task.html'
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        print(self.request.user)
        return super().form_valid(form)


class DetailTask(FormMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'get_article'
    form_class = CommentFormTask

    def get_success_url(self, **kwargs):
        return reverse_lazy('detail', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.question = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class MyLoginView(LoginView):
    form_class = AuthenticationForm


class EmailVerify(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('home')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

