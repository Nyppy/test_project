from django import forms
from .models import User_reg, User_auth_one, User_read, User_read_pass, Post, Post_search_r


class UserForm(forms.ModelForm):
    class Meta:
        model = User_reg
        fields = ('username', 'password', 'email', 'first_name', 'last_name')


class UserUp(forms.ModelForm):
    class Meta:
        model = User_auth_one
        fields = ('username', 'password')


class UserRead(forms.ModelForm):
    class Meta:
        model = User_read
        fields = ('username', 'email', 'first_name', 'last_name')


class UserReadPass(forms.ModelForm):
    class Meta:
        model = User_read_pass
        fields = ('password1', 'password2')


class Form_new_posts(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')


class Form_serach_posts(forms.ModelForm):
    class Meta:
        model = Post_search_r
        fields = ('text',)


class PostCategories(forms.Form):
    OPTIONS = (
        ("Programming", "Программирование"),
        ("Science", "Наука"),
        ("Life", "Жизнь"),
        ("Technology", "Технологии"),
        ("Security", "Безопасность"),
        ("Computer", "Компьютеры"),
    )

    Categories = forms.MultipleChoiceField(widget=forms.Select,
                                          choices=OPTIONS)
