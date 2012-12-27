from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # GET params for filter, like: ?cat=hardware or ?search=searchterm
    # /event/2012_05_02_6/
    url(r'^event/(?P<eventslug>.*)/$', 'comicApp.views.SpecificEvent'),
    
    # /event/2012_05_02_6/edit/
    url(r'^event/(?P<eventslug>.*)/edit$', 'comicApp.views.EditEvent'),
    
    # /edit/comic_15
    url(r'^edit/comic_(?P<comicId>.*)$', 'comicApp.views.EditComic'),
    
    # /user/myusername
    url(r'^user/(?P<username>.*)/$', 'comicApp.views.UserProfile'),
    
    # /user_search
    url(r'^user_search/$', 'comicApp.views.UserSearch'),
    
    # just domain
    url(r'^$', 'comicApp.views.MainView'),
    
    # vote_up
    url(r'^vote_up$', 'comicApp.views.VoteUp'),
    
   #url(r'^sign_in/', ''),
   
    url(r'^admin/', include(admin.site.urls)),

    #All Auth URLS
    url(r'^accounts/', include('allauth.urls')),
)

handler404 = 'comicApp.views.Custom404'
