import django_tables2 as tables
from .models import YhForm

class FormTable(tables.Table):
    class Meta:
        model = YhForm

        exclude = ['created','updated']

