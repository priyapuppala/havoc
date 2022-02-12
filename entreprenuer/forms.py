from django import forms
from .models import *


class EntreprenuerForm(forms.ModelForm):
    class Meta:
        model = Entreprenuer
        fields = "__all__"
        labels = {
            'fullname': "Name",
            'password': "Password",
            'email': "Email",
            'mobileno': "Mobile",
            'location': "Location",
        }
        widgets = {
            'password': forms.PasswordInput(),
        }


class EntreprenuerLoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


class EntreprenuerContactForm(forms.ModelForm):
    class Meta:
        model = EntreprenuerContact
        fields = "__all__"
        widgets = {
            'firstname': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'lastname': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
            'query': forms.Textarea(attrs={'placeholder': 'Message'}),
        }
        labels = {
            'firstname': "",
            'lastname': "",
            'email': "",
            'subject': "",
            'query': "",
        }


class EntreprenuerIdeasForm(forms.ModelForm):
    class Meta:
        model = EntreprenuerIdeas
        exclude = ('fullname', 'email', 'mobileno', 'location','invmail',)
        labels = {
            'about': 'About Yourself and StartUp',
            'resume': 'Resume',
            'ideacat': "Business System / Category",
            'ideadesc': "StartUp Description",
            'ideaname': "Idea Name",
        }
        widgets = {
            'about': forms.Textarea(
                attrs={'placeholder': 'Describe about you and your work towards the startup intiative'}),
        }
