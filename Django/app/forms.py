import warnings
from django.forms import ModelForm
from allauth.account.forms import LoginForm, SignupForm
from django import forms
from app.models import UserProfile, EcfData, ModuleData, Files, PublicEcf
from datetime import date
from django.forms.widgets import DateInput
from django.utils.translation import pgettext, ugettext, ugettext_lazy as _


class MyLoginForm(LoginForm):
    def login(self, *args, **kwargs):
        self.fields['login'].widget = forms.TextInput(attrs={'type': 'email', 'class': 'form-control'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        return super(MyLoginForm, self).login(*args, **kwargs)

class MySignupForm(SignupForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    dob = forms.DateTimeField(widget=forms.SelectDateWidget)
    userpower = forms.IntegerField()


    def clean(self):
        emailx = str(self.cleaned_data['email'])
        domain = emailx.split('@')[1]
        if domain != "sheffield.ac.uk":
            self.add_error(
                    'email', _("You must use your @sheffield.ac.uk email")
                )
            return self

    def save(self, request):

        # Ensure you call the parent classes save.
        # .save() returns a User object.
        user = super(MySignupForm, self).save(request)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        UserProfile.objects.create(user=user)
        user.profile.userpower = self.cleaned_data['userpower']
        user.profile.dob = self.cleaned_data['dob']
        user.profile.save()
        return user



class NewEcf(forms.Form):
    ukvisa = forms.IntegerField()
    coursename = forms.CharField(max_length=255)
    studyyear = forms.IntegerField()
    numberofunits = forms.IntegerField()
    durationenddate = forms.DateTimeField(widget=forms.SelectDateWidget)
    durationstartdate = forms.DateTimeField(widget=forms.SelectDateWidget)
    circumstance = forms.IntegerField()
    detailecf = forms.CharField(max_length=10000)
    fileinput = forms.FileField()


    # declaration = forms.BooleanField()

    # unitcode1 = forms.CharField(max_length=10)
    # type1 = forms.CharField(max_length=10)
    # startdate1 = forms.DateTimeField(widget=forms.SelectDateWidget)
    # enddate1 = forms.DateTimeField(widget=forms.SelectDateWidget)
    # action1 = forms.CharField(max_length=4)

    def __init__(self, *args, **kwargs):
        self.units_no = kwargs.pop('units_no')
        super(NewEcf, self).__init__(*args, **kwargs)
        for i in range(1,self.units_no+1):
            self.fields['unitcode' + str(i)] = forms.CharField(max_length=255)
            # unitcode = forms.CharField(max_length=10)
            self.fields['type' + str(i)] = forms.CharField(max_length=255)
            self.fields['startdate' + str(i)] = forms.DateTimeField(widget=forms.SelectDateWidget)
            self.fields['enddate' + str(i)] = forms.DateTimeField(widget=forms.SelectDateWidget)
            self.fields['action' + str(i)] = forms.CharField(max_length=4)

class PublicForm(forms.Form):
        publicecf = forms.CharField(max_length=10000)


class EditModule(forms.Form):
        modid = forms.IntegerField(widget=forms.HiddenInput())
        action = forms.CharField()
        approved = forms.IntegerField()

class EditProfile(forms.Form):
        # email = forms.EmailField()
        first_name = forms.CharField()
        last_name = forms.CharField()
        dob = forms.DateTimeField(widget=forms.SelectDateWidget)

class extraUpload(forms.Form):
        fileinput = forms.FileField()

class requestUpload(forms.Form):
        moreproof = forms.BooleanField()
