from django.shortcuts import render
from users.models import Teacher_Profile
from informing_app.models import News_Announce

def index(request):
    news = News_Announce.objects.all()
    return render(request, 'base_app/main.html', context={'news': news})

