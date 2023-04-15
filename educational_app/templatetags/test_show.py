from django import template

register = template.Library()

@register.filter
def get_item_by_index(seq, index):
    return seq[index]