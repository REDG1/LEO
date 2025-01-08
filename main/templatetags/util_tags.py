from django import template
from django.conf import settings
import os


register = template.Library()


@register.simple_tag
def getDebug():
  print("debug:", settings.DEBUG)
  return settings.DEBUG

@register.filter(name='get_static_files')
def get_static_files(static_type):
    """
    Retrieve static files from the Vue build directory.
    """
    vue_dir = os.path.join(settings.BASE_DIR, "main" , "static", "vue")
    assets_dir = os.path.join(vue_dir, "assets")

    result = []
    if os.path.exists(vue_dir):
        result.extend([f"vue/{f}" for f in os.listdir(vue_dir) if f.endswith(static_type)])
    if os.path.exists(assets_dir):
        result.extend([f"vue/assets/{f}" for f in os.listdir(assets_dir) if f.endswith(static_type)])
    print(vue_dir)
    print(assets_dir)
    print(result)

    return result