from django import template

register = template.Library()

@register.filter
def negative(value):
    try:
        return -int(value)
    except (ValueError, TypeError):
        return value  # Return the original value if conversion fails

@register.filter
def range_filter(value):
    return range(value)