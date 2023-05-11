import time
from datetime import datetime
from django.http import HttpResponse
import json

def get_time(request):
    # date = datetime.utcnow()
    # return HttpResponse(int(time.mktime(date.timetuple())) * 1000, content_type='application/json')
    return HttpResponse(datetime.now().strftime("%B %d, %Y %H:%M:%S"))