from django import template

register = template.Library()


@register.filter
def plural(num, choices):
    choices = choices.split(",")
    num = abs(int(num))

    if num % 10 == 1 and num % 100 != 11:
        return f'{num} {choices[0]}'
    elif num % 10 >= 2 and num % 10 <= 4 and \
            (num % 100 < 10 or num % 100 >= 20):
        return f'{num} {choices[1]}'
    else:
        return f'{num} {choices[2]}'