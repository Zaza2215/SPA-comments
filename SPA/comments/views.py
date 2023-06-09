from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, PageNotAnInteger

from .models import Profile, Comment
from .forms import LoginUserForm, RegisterUserForm, AddCommentForm


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'comments/register.html'
    success_url = reverse_lazy('main')


class UserLoginView(LoginView):
    form_class = LoginUserForm
    template_name = 'comments/login.html'

    def get_success_url(self):
        return reverse_lazy('main')


def logout_user(request):
    logout(request)
    return redirect('main')


class CommentBase(View):
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        sort_by = self.request.GET.get('sort_by', '-created_time')
        object_list2 = Comment.objects.filter(parent=None).prefetch_related('replies__replies').order_by(sort_by)

        paginator = Paginator(object_list2, 15)
        page = request.GET.get('page')
        object_list = paginator.get_page(page)

        context = {
            'object_list': object_list,
        }
        if request.user.is_authenticated:
            context['form'] = AddCommentForm
        return render(request, 'comments/index.html', context=context)

    def post(self, request, *args, **kwargs):
        sort_by = self.request.GET.get('sort_by', '-created_time')
        object_list = Comment.objects.filter(parent=None).prefetch_related('replies__replies').order_by(sort_by)

        paginator = Paginator(object_list, 15)
        page = request.GET.get('page')
        object_list = paginator.get_page(page)

        context = {
            'object_list': object_list,
        }
        if request.user.is_authenticated:
            form = AddCommentForm(request.POST, request.FILES)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.save()
        else:
            form = AddCommentForm
        context['form'] = form
        return render(request, 'comments/index.html', context=context)
