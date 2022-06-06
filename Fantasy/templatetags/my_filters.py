from django import template

register = template.Library()

@register.filter()
def is_numeric(value):
    return isinstance(value, int) or value.isdigit()


@register.filter()
def is_in_keys(d, value):  
   return value in d.keys()