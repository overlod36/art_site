from django.shortcuts import render
from users.models import Teacher_Profile

def index(request):
    return render(request, 'base_app/base.html')

