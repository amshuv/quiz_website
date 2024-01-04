from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms
from django.forms import ModelForm
from .models import Player, User, QuesModel, ResultModel


class PlayerSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email_id = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def data_save(self):
        user = super().save(commit=True)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.is_player = True
        user.save()
        player = Player.objects.create(user=user)
        player.first_name =  self.cleaned_data.get('first_name')
        player.last_name = self.cleaned_data.get('last_name')
        player.email_id = self.cleaned_data.get('email_id')
        player.save()
        return user

class addQuestionform(ModelForm):
    class Meta:
        model = QuesModel
        fields = "__all__"


class ResultForm(forms.ModelForm):
    class Meta:  # provides additional info forms
        model = ResultModel   # specifies form associated with result model
        fields = []
 # specifies which field should be included in the form