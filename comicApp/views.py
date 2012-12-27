from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.db.models import Q
from django.template import RequestContext
from comicApp.models import Event, Comic, Category, User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def VoteUp(request):
    ret_msg = -1
    if request.is_ajax():
        if request.method == 'POST':
            c_id = request.POST.get('id')
            #add vote to comic.id == c_id
            try:
            	    comic = get_object_or_404(Comic, pk=c_id)
            except (Comic.DoesNotExist):
            	    ret_msg = -1
            else:
            	    comic.votes_up += 1
            	    comic.save()
            	    ret_msg = comic.votes_up

    return HttpResponse(content=ret_msg, status=200)

def SpecificEvent(request, eventslug):

        event = get_object_or_404(Event, slug=eventslug)
        
        if request.method == 'GET':
                 searchTerm = request.GET.get('search')
                 category = request.GET.get('cat')
                 searchUser = request.GET.get('search_user')
                 started = request.GET.get('f')
        
        if category and searchTerm:
        	event_list = Event.objects.filter(Q(title__contains=searchTerm) & Q(categories__name=category)).order_by('date', 'title')
        	get_param = '?cat='+category+'&search='+searchTerm
        	eventNext = Event.objects.filter(((Q(date=event.date) & Q(title__gt=event.title)) | Q(date__gt=event.date)) & Q(title__contains=searchTerm) & Q(categories__name=category)).order_by('date', 'title')[:1]
                eventPrev = Event.objects.filter(((Q(date=event.date) & Q(title__lt=event.title)) | Q(date__lt=event.date))  & Q(title__contains=searchTerm) & Q(categories__name=category)).order_by('date', 'title').reverse()[:1]
        elif category:
        	event_list = Event.objects.filter(categories__name=category).order_by('date', 'title')
        	get_param = '?cat='+category
		eventNext = Event.objects.filter(((Q(date=event.date) & Q(title__gt=event.title)) | Q(date__gt=event.date)) & Q(categories__name=category)).order_by('date', 'title')[:1]
                eventPrev = Event.objects.filter(((Q(date=event.date) & Q(title__lt=event.title)) | Q(date__lt=event.date))  & Q(categories__name=category)).order_by('date', 'title').reverse()[:1]         
        elif searchTerm:
        	event_list = Event.objects.filter(title__contains=searchTerm).order_by('date', 'title')
        	get_param = '?search='+searchTerm
        	eventNext = Event.objects.filter(((Q(date=event.date) & Q(title__gt=event.title)) | Q(date__gt=event.date)) & Q(title__contains=searchTerm)).order_by('date', 'title')[:1]
                eventPrev = Event.objects.filter(((Q(date=event.date) & Q(title__lt=event.title)) | Q(date__lt=event.date))  & Q(title__contains=searchTerm)).order_by('date', 'title').reverse()[:1]
        elif searchUser:
        	return HttpResponseRedirect("/user_search/?search_user="+searchUser)
	else:
        	eventNext = Event.objects.filter((Q(date=event.date) & Q(title__gt=event.title)) | Q(date__gt=event.date)).order_by('date', 'title')[:1]
                eventPrev = Event.objects.filter((Q(date=event.date) & Q(title__lt=event.title)) | Q(date__lt=event.date)).order_by('date', 'title').reverse()[:1]
                event_list = Event.objects.all().order_by('date', 'title')
                get_param = ''
       
        if event_list and started and get_param: 
        		if not event.id == event_list[0].id:
        			event = event_list[0]
        			return HttpResponseRedirect("/event/"+event.slug+"/"+get_param)
        
        next = None
        if eventNext:
        	next = eventNext[0].slug
        
        prev = None
        if eventPrev:
        	prev = eventPrev[0].slug
        
        comics = Comic.objects.filter(event=event)
        
        categories = Category.objects.all();
        
        context = {'event': event, 'comics': comics, 'next': next, 'prev': prev, 'list': event_list, 'categories': categories, 'get_param': get_param, 'search_term': searchTerm, 'category': category}
        return render_to_response('showevent.html', context, context_instance=RequestContext(request))


def UserSearch(request):
	if request.method == 'GET':
                 searchTerm = request.GET.get('search')
                 category = request.GET.get('cat')
                 searchUser = request.GET.get('search_user')
                 
        if searchUser:
        	 comic_list = Comic.objects.filter(user__name__contains=searchUser).order_by('user__name')
        	 get_param = '?search_user='+searchUser
        elif searchTerm and category:
        	return HttpResponseRedirect("/?search="+searchTerm+"&cat="+category+"&f=started")
        elif searchTerm:
        	return HttpResponseRedirect("/?search="+searchTerm+"&f=started")
        elif category:
        	return HttpResponseRedirect("/?cat="+category+"&f=started")
        else:
        	 comic_list = Comic.objects.all().order_by('user__name')
        	 get_param = ''
        	 
        categories = Category.objects.all();
        	 
        context = {'comic_list':comic_list, 'categories': categories, 'get_param': get_param, 'search_user': searchUser}
        return render_to_response('usersearch.html', context, context_instance=RequestContext(request))

def MainView(request):

	if request.method == 'GET':
                 searchTerm = request.GET.get('search')
                 category = request.GET.get('cat')
                 searchUser = request.GET.get('search_user')
                 
        if category and searchTerm:
        	event_list = Event.objects.filter(Q(title__contains=searchTerm) & Q(categories__name=category)).order_by('date', 'title')
                get_param = '?cat='+category+'&search='+searchTerm
        elif category:
        	event_list = Event.objects.filter(categories__name=category).order_by('date', 'title')
                get_param = '?cat='+category
        elif searchTerm:
        	event_list = Event.objects.filter(title__contains=searchTerm).order_by('date', 'title')
                get_param = '?search='+searchTerm
        elif searchUser:
        	return HttpResponseRedirect("/user_search/?search_user="+searchUser)
        else:
                event_list = Event.objects.all().order_by('date', 'title')
                get_param = ''
                
        if event_list and get_param:  
        		return HttpResponseRedirect("/event/"+event_list[0].slug+"/"+get_param)
                
        categories = Category.objects.all();
	
	context = {'list': event_list, 'categories': categories, 'get_param': get_param, 'search_term': searchTerm, 'category': category}
        return render_to_response('index.html', context, context_instance=RequestContext(request))
        
        
def UserProfile(request, username):
	
	if request.method == 'GET':
                 searchTerm = request.GET.get('search')
                 category = request.GET.get('cat')
                 searchUser = request.GET.get('search_user')
                 
        if searchUser:
        	return HttpResponseRedirect("/user_search/?search_user="+searchUser)
        elif searchTerm and category:
        	return HttpResponseRedirect("/?search="+searchTerm+"&cat="+category+"&f=started")
        elif searchTerm:
        	return HttpResponseRedirect("/?search="+searchTerm+"&f=started")
        elif category:
        	return HttpResponseRedirect("/?cat="+category+"&f=started")

	u = get_object_or_404(User, name = username)
	comic_list = Comic.objects.filter(user=u).order_by('event__date', 'event__title')
	
	categories = Category.objects.all();
	
	context = {'c_list': comic_list, 'categories': categories, 'user': u}
        return render_to_response('profile.html', context, context_instance=RequestContext(request))
        
        
def EditEvent(request, eventslug):
	event = Event.objects.get(slug=eventslug)
	context = {'event': event}
        return render_to_response('editevent.html', context, context_instance=RequestContext(request))
            
def EditComic(request, comicId):
	comic = Comic.objects.get(id=comicId)
	context = {'comic': comic}
        return render_to_response('editcomic.html', context, context_instance=RequestContext(request))
        
        
def Custom404(request):
	context = {}
        return render_to_response('my404.html', context, context_instance=RequestContext(request))
