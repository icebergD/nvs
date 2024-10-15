from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from mainapp.models import Table, Field, Permision

@api_view(['POST'])
# @permission_classes((IsAuthenticated, ))
def Hello(request):
    if request.method == 'POST':
        print(request.data)

        return Response({'response': "good"})
    return Response({'response': "bad"})


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def PermisionList(request):
    if request.method == 'GET':
        permision_list = Permision.objects.filter(user=request.user.id).values()
        return Response({'permision_list': permision_list})
    return Response({'response': "error"})


class test(View):
    def get(self, request, *args, **kwargs):
        return render(request, "apiapp/test.html")
