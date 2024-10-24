from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Return the value for the given key in the dictionary."""
    return dictionary.get(key)

@register.filter
def multiply(value, arg):
    """Multiply the value by the arg."""
    try:
        return value * arg
    except (TypeError, ValueError):
        return None  

@register.filter
def length_is(value, arg):
    """Check if the length of the value is equal to arg."""
    try:
        return len(value) == int(arg)
    except (ValueError, TypeError):
        return False

