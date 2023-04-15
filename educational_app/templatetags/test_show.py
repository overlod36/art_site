from django import template

register = template.Library()

@register.filter
def get_index(seq, index):
    return seq[index]