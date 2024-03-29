from __future__ import absolute_import  # Python 2 only
from jinja2 import Environment
from Django.contrib.staticfiles.storage import staticfiles_storage
from Django.core.urlresolvers import reverse

def environment(**options):
    env = Environment(**options)
    env.globals.update({
       'static': staticfiles_storage.url,
       'url': reverse,
    })
    return env