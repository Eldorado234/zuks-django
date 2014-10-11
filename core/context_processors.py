from django.conf import settings

def base_settings(request):
  return {'settings': settings}
