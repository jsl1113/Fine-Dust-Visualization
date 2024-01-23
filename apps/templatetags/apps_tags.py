from django import template

from ..models import district_info
from ..models import school_info

register = template.Library()

@register.tag
def district_list():
    district = [("동부"), ("south"), ("north")]
    return district
