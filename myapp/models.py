from django.db import models
from django.conf import settings
from django.utils import timezone
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


class User_reg(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class User_auth_one(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class User_read(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class User_read_pass(models.Model):
    password1 = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    categories = models.CharField(max_length=400)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Post_search_r(models.Model):
    text = models.CharField(max_length=100)


class Categories(models.Model):
    categories = models.CharField(max_length=400)
    post = models.CharField(max_length=400)

    def __str__(self):
        return self.categories



# API
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ['created']
