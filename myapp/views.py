from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import View
from rest_framework import viewsets, generics
from .serializers import PostSerializer
from .permissions import IsOWnOrReadOnly
# примесь для проверки пользователя
from rest_framework.permissions import IsAuthenticated
# примесь для проверки администратора
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication

from .forms import UserForm, UserRead, UserReadPass, Form_new_posts, Form_serach_posts, PostCategories
from .models import Post, Categories


class Index(View):
    def get(self, request):
        form_s = Form_serach_posts()
        return render(request, 'myapp/index.html', {'form_s': form_s})

    def post(self, request):
        form_s = Form_serach_posts(request.POST)
        if form_s.is_valid():
            return redirect('search_post', search=request.POST['text'])
        return render(request, 'myapp/index.html', {'form_s': form_s})


class Register(View):
    def post(self, request):
        form = UserForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(username=request.POST['username'],
                                            password=request.POST['password'],
                                            email=request.POST['email'],
                                            first_name=request.POST['first_name'],
                                            last_name=request.POST['last_name'])

            user.save()

            group = Group.objects.get(name='All User')
            user.groups.add(group)

            return redirect('index')

    def get(self, request):
        form = UserForm()
        return render(request, 'myapp/forms.html', {'form': form})


class GetAuthUser(View):
    err = 'Введенные данные неверны, повторите вход!'

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())

            return render(request, 'myapp/index_auth.html', {})
        else:
            form = AuthenticationForm()

            return render(request, 'myapp/forms_auth.html', {'err': self.err, 'form': form})

    def get(self, request):
        form = AuthenticationForm()

        return render(request, 'myapp/forms_auth.html', {'form': form})


class OutUser(View):
    def get(self, request):
        auth.logout(request)

        return redirect('index')


class ImUser(View):

    def get(self, request):
        username = request.user.username
        last_name = request.user.last_name
        first_name = request.user.first_name
        email = request.user.email

        form_s = Form_serach_posts()
        form_pass = UserReadPass()
        form = UserRead()
        me = User.objects.get(username='admin')
        posts = Post.objects.filter(author=me)

        form.initial['username'] = username
        form.initial['first_name'] = first_name
        form.initial['last_name'] = last_name
        form.initial['email'] = email

        return render(request, 'myapp/index_im.html', {'username': username, 'last_name': last_name,
                                                       'first_name': first_name, 'email': email,
                                                       'form': form, 'form_pass': form_pass, 'posts': posts,
                                                       'form_s': form_s})

    def post(self, request):
        form = UserRead(request.POST)
        form_pass = UserReadPass(request.POST)
        form_s = Form_serach_posts(request.POST)

        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user.username = request.POST['username']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']

            user.save()

            return render(request, 'myapp/index_im.html', {'form': form, 'form_pass': form_pass})

        form_user = UserRead()
        form_user.initial['username'] = request.user.username
        form_user.initial['first_name'] = request.user.first_name
        form_user.initial['last_name'] = request.user.last_name
        form_user.initial['email'] = request.user.email

        if form_s.is_valid():
            return redirect('search_post', search=request.POST['text'])

        try:
            paser = request.POST['password1'] == request.POST['password2']
        except Exception as e:
            return render(request, 'myapp/index_im.html', {'form': form, 'form_pass': form_pass, 'form_s': form_s})
        else:
            if form_pass.is_valid():
                user_pass = User.objects.get(username=request.user.username)

                if request.POST['password1'] == request.POST['password2']:
                    user_pass.set_password(request.POST['password1'])
                    user_pass.save()

                    return redirect('auth_user')

            return render(request, 'myapp/index_im.html', {'form': form_user, 'form_pass': form_pass, 'form_s': form_s})


class NewPosts(View):

    def get(self, request):
        form = Form_new_posts()
        form_cat = PostCategories()

        return render(request, 'myapp/new_posts.html', {'form': form, 'form_cat': form_cat})

    def post(self, request):
        form = Form_new_posts(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.categories = request.POST['Categories']
            post.published_date = timezone.now()
            post.publish()

            cat = Categories(categories=request.POST['Categories'])
            cat.post = post.pk
            cat.save()
        return redirect('post', pk=post.pk)


class AllPosts(View):

    def get(self, request):
        form_s = Form_serach_posts()
        posts = Post.objects.all().order_by("-published_date")
        return render(request, 'myapp/all_posts.html', {'posts': posts, 'form_s': form_s})

    def post(self, request):
        form_s = Form_serach_posts(request.POST)
        if form_s.is_valid():
            return redirect('search_post', search=request.POST['text'])
        return render(request, 'myapp/index.html', {'form_s': form_s})


class GetPosts(View):

    def get(self, request, pk):
        elem = Post.objects.get(pk=pk)

        return render(request, 'myapp/posts.html', {'post': elem})


class SearchPost(View):

    def get(self, request, search):
        form_s = Form_serach_posts()
        list_post = list()
        for i in Categories.objects.filter(categories=search):
            list_post.append(Post.objects.get(pk=i.post))

        return render(request, 'myapp/post_s.html', {'posts': list_post, 'form_s': form_s})

    def post(self, request, search):
        form_s = Form_serach_posts(request.POST)
        list_post = list()
        for i in Categories.objects.filter(categories=search):
            list_post.append(Post.objects.get(pk=i.post))

        if form_s.is_valid():
            return redirect('search_post', search=request.POST['text'])
        return render(request, 'myapp/post_s.html', {'posts': list_post, 'form_s': form_s})


class GetCategories(View):

    def get(self, request):
        form_s = Form_serach_posts()
        categories = Categories.objects.all()

        return render(request, 'myapp/all_categories.html', {'form_s': form_s, 'cat': categories})

    def post(self, request):
        form_s = Form_serach_posts(request.POST)
        if form_s.is_valid():
            return redirect('search_post', search=request.POST['text'])
        return render(request, 'myapp/index.html', {'form_s': form_s})


class GetCategoriesOne(View):

    def get(self, requests, pk):
        cat = set()

        cc = Categories.objects.get(pk=pk).categories
        categories = Categories.objects.filter(categories=cc)

        for i in range(1, len(categories)):
            cat.add(Post.objects.get(pk=categories[i].post))

        return render(requests, 'myapp/categories_one.html', {'cat': cat})


# class API
class PostCreate(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, )


class PostAll(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # доступ только через токены, но еще можно указать доступные способы аутентификации для всего проекта
    # в settings.py в DEFAULT_AUTHENTICATION_CLASSES
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
