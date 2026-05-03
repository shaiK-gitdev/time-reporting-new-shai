from dataclasses import fields
from multiprocessing.spawn import import_main_path
from pyexpat import model
from rest_framework.serializers import ModelSerializer
from base.models import YhForm

class FormSerializer(ModelSerializer):
    class Meta:
        model = YhForm
        fields = '__all__'
