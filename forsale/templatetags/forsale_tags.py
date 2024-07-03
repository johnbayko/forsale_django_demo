from django import template

register = template.Library()

@register.filter(name="format_cents")
def format_cents(value):
    dollars = value // 100
    cents = value % 100
    return f"${dollars:,}.{cents:02}"

