
from urllib import response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import YhForm
from .serializers import FormSerializer
@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET / api',
        'GET /api/yhform',
        'GET /api/yhform/:id',

    ]
    return Response(routes)

@api_view(['GET'])
def getForms(request):
    forms = YhForm.objects.all()
    serializer = FormSerializer(forms,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getForm(request,pk):
    form = YhForm.objects.get(id=pk)
    serializer = FormSerializer(form)
    return Response(serializer.data)