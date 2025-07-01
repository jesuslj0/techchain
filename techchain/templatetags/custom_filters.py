from django import template
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def timesince_short(value):
    return timesince(value).split(',')[0]  # Solo la primera unidad
