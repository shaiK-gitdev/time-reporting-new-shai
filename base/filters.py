import django_filters 
from django_filters  import DateFilter,CharFilter
from .models import *
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class FormFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date',
                            widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                            lookup_expr='gte', label='Start Date')
    end_date = DateFilter(field_name='date',
                          widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                          lookup_expr='lte', label='End Date')

    class Meta:
        model = YhForm
        fields = '__all__'
        exclude = ['updated','created','date']
        
  

