from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.views.generic.list_detail import object_list
from voting.views import vote_on_object
from dajaxice.core import dajaxice_autodiscover
from django.conf import settings
from cars.models import Comment
from cars.forms import ProfileForm

dajaxice_autodiscover()

urlpatterns = patterns('',
    (r'^cars/$', 'cars.views.index'),
    (r'^cars/(?P<id>\d+)/$', 'cars.views.detail'),
    (r'^cars/gallery/(?P<id>\d+)/$', 'cars.views.gallery'),
    (r'^cars/ranking/$', 'cars.views.rank'),
    (r'^cars/about/$', 'cars.views.about'),
    (r'^cars/(?P<id>\d+)/edit/$', 'cars.views.edit'),
    (r'^cars/home/$', 'cars.views.home'),
    (r'^cars/upload/(?P<id>\d+)/$', 'cars.views.upload_file'), 
    (r'^cars/test/(?P<id1>\d+)/(?P<id2>\d+)/$', 'cars.views.compare'), #Ivan
    (r'^cars/(?P<id1>\d+)/(?P<id2>\d+)/$', 'cars.views.compare'),
    (r'^cars/(?P<id>\d+)/rate/$', 'cars.views.rate'),
  
    #(r'^cars/links/?$', object_list, dict(queryset=Comment.objects.all(),
    #    template_object_name='comment', template_name='cars/comments.html',
    #    paginate_by=15, allow_empty=True)),

    #(r'^cars/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$',
    #    vote_on_object, dict(model=Comment, template_object_name='comment',
    #        template_name='cars/comments.html',
    #        allow_xmlhttprequest=True)),

    # Search urls:
    (r'^cars/search/$', 'cars.views.search'),
    (r'^cars/(?P<id>\d+)/search/$', 'cars.views.search'),
    (r'^cars/(?P<id>\d+)/edit/search/$', 'cars.views.search'),
    (r'^cars/upload/search/$', 'cars.views.search'), 
    (r'^cars/(?P<id1>\d+)/(?P<id2>\d+)/search/$', 'cars.views.search'),
    (r'^cars/accounts/login/search/$', 'cars.views.search'),
    (r'^cars/accounts/register/search/$', 'cars.views.search'),
    (r'^cars/ranking/search/$', 'cars.views.search'),
    (r'^cars/about/search/$', 'cars.views.search'),
#    (r'^cars/tracking/', include('tracking.urls')),
    url(r'^cars/admin/', include(admin.site.urls)),
    (r'^cars/accounts/', include('registration.urls')),

    (r'^index/$', direct_to_template,
            { 'template': 'index.html' }, 'index'),

    #('^cars/profiles/edit', 'profiles.views.edit_profile', {'form_class': ProfileForm,'success_url':'/my/custom/url',}),
    #(r'^cars/profiles/', include('profiles.urls')),
    
    # Dajax urls:
    (r'^cars/dajax/', include('dajaxice.urls')),      
	)

#if settings.DEBUG: 
    #urlpatterns += patterns('', 
       #(r'%s(?P<path>.*)' % settings.MEDIA_URL[1:], 'cars.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    #)

