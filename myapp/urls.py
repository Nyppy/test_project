from django.urls import path, include
from . import views
from djoser import views as djViwe

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('register/', views.Register.as_view(), name='register'),
    path('auth_user/', views.GetAuthUser.as_view(), name='auth_user'),
    path('out_user/', views.OutUser.as_view(), name='out_user'),
    path('im/', views.ImUser.as_view(), name='im_user'),
    path('new_posts/', views.NewPosts.as_view(), name='new_posts'),
    path('all_posts/', views.AllPosts.as_view(), name='all_posts'),
    path('post/<int:pk>/', views.GetPosts.as_view(), name='post'),
    path('search_post/<str:search>/', views.SearchPost.as_view(), name='search_post'),
    path('categories/', views.GetCategories.as_view(), name='categories'),
    path('categories_one/<int:pk>/', views.GetCategoriesOne.as_view(), name='categories_one'),

    # создание поста
    path('api/post_create/', views.PostCreate().as_view()),
    # вывод всех постов
    path('api/post_all/', views.PostAll().as_view()),
    path('api/auth/', include('djoser.urls')),
    path('api/auth_token/', include('djoser.urls.authtoken')),
    path('api/qwer/', djViwe.TokenDestroyView.as_view()),
]

'''
Регистрация происходит путем отправки JSON {"email": "","username": "","password": ""}
по адресу http://127.0.0.1:8000/api/auth/users/
в ответ ничего не отсылается

Вход происходит путем отправки JSON {"username": "","password": ""}
по адресу http://127.0.0.1:8000/api/auth_token/token/login/
в ответете отсылается веб-токен

Выход происходит путем отправки вет токена в headers по адресу 
http://127.0.0.1:8000/api/auth_token/token/logout/
'''