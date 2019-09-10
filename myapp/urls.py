from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', views.UserViewsSet)
router.register(r'post', views.PostViewsSet)
# router.register(r'add_post', views.PostAddViewsSet)

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
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
