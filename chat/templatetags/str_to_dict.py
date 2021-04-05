from django import template
import json

register = template.Library()

@register.filter(name='string_to_dict')
def string_to_dict(value, key):
  """
    Returns the value turned into a list.
  """

  return json.loads(value).get(key) #value.split(key)