
from django import forms
from django.forms import ModelForm
from .models import Title,YhForm,UserTitle
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelChoiceField

from django.core.exceptions import ValidationError

from datetime import date

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class DateInput(forms.DateInput):
    input_type = 'date'



class TitForm(ModelForm):
    class Meta:
        model = Title
        fields = '__all__'
        exclude = ['updated','created']
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        if " - " not in name:
                raise ValidationError(
                    "Title should be xxx - xxx format."
                )    
        
class FillForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FillForm, self).__init__(*args, **kwargs)

        if user:
            user_titles = UserTitle.objects.filter(user=user)
            title_choices = [(user_title.title.id, user_title.title.name) for user_title in user_titles]
            self.fields['title'] = ModelChoiceField(queryset=Title.objects.filter(id__in=[title[0] for title in title_choices]))
        # Set initial value for date field to today's date
        self.fields['date'].initial = date.today()

    class Meta:
        model = YhForm
        fields = '__all__'
        exclude = ['username', 'created', 'updated', 'gl', 'dm']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }

    
       

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email',]
        

        

       