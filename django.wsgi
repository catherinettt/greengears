#!/usr/bin/env python
import os, sys

# make sure app's modules can be found
sys.path.append('/home/greengears')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Switch to the directory of your project. (Optional.)
# os.chdir("/home/ivanma/greengears")

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
