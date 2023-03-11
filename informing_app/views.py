from django.shortcuts import render
from . models import Course_Announce

def announces(request):
    announces = Course_Announce.objects.all()
    context = { 'announces': announces }
    return render(request, 'informing/announces.html', context)
