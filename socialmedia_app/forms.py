from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from socialmedia_app.models import Account, Post


class RegistrationForm(UserCreationForm):
    # email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')
    age = forms.IntegerField()
    country = forms.CharField(max_length=255)
    height = forms.IntegerField()

    class Meta:
        model = Account
        fields = ['user_email', 'username', 'age',
                  'country', 'height', 'password1', 'password2']

    # def clean_email(self):
    #   user_email = self.cleaned_data['email'].lower()
    #   try:
    #     account = Account.objects.exclude(pk=self.instance.pk).get(user_email=user_email)
    #   except Account.DoesNotExist:
    #     return user_email
    #   raise forms.ValidationError('Email "%s" is already in use.' % account)

    # def clean_username(self):
    #   username = self.cleaned_data['username']
    #   try:
    #     account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
    #   except Account.DoesNotExist:
    #     return username
    #   raise forms.ValidationError('Username "%s" is already in use.' % username)


# class AccountAuthenticationForm(forms.ModelForm):

#   password = forms.CharField(label='Password', widget=forms.PasswordInput)

#   class Meta:
#     model = Account
#     fields = ('user_email', 'password')

    # def clean(self):
    #   if self.is_valid():
    #     user_email = self.cleaned_data['user_email']
    #     password = self.cleaned_data['password']
    #     if not authenticate(email=user_email, password=password):
    #       raise forms.ValidationError("Invalid login")

# create a new post

        # text = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder':'what you reckon?'}), label='', help_text="word limit : 500")
        # media = forms.ImageField(label="image", required=False)
        # user = forms.CharField(widget=forms.HiddenInput(), required=False)

        # def save(self, user, time):
        #     text = self.cleaned_data['text']
        #     media = self.cleaned_data['media']
        #     post = Post(user=user, date_Post=time, text=text, media=media,)
        #     post.save()

        # text = forms.CharField(
        #     label='',
        #     # creating a widget box to get input text
        #     widget=forms.Textarea(attrs={
        #         'rows': '5',
        #         'placeholder': 'Input your thoughts here...'
        #         }))

        # image = forms.ImageField(required=False)

        # class Meta:
        #     model = Post
        #     fields = ['body, image']

class NewPostForm(forms.ModelForm):
    text = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '5',
            'placeholder': 'Input your thoughts here...'
        }))

    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['text', 'image']
