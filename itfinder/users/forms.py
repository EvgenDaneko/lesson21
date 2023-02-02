from django.forms import ModelForm
from .models import Profile, Skill
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):  # Создание Users
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name'
        }

    def int(self, *args, **kwargs):
        super(CustomUserCreationForm, self).init(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username',
                  'city', 'bio', 'intro', 'image',
                  'github', 'likedin', 'twitter',
                  'youtube', 'website']

        def int(self, *args, **kwargs):
            super(ProfileForm, self).init(*args, **kwargs)

            for name, field in self.fields.items():
                field.widget.attrs.update({'class': 'input'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = 'all'
        exclude = ['owner']

    def int(self, *args, **kwargs):
        super(SkillForm, self).init(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
