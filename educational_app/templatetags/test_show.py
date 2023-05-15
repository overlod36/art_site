from django import template
from educational_app.models import Task, Task_Attempt

register = template.Library()

@register.filter
def get_item_by_index(seq, index):
    return seq[index]
