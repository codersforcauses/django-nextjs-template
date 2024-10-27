from django.http import HttpResponse
from rest_framework.decorators import api_view


# Create your views here.
@api_view(["GET"])
def ping(request):
    return HttpResponse("Pong!", status=200)
