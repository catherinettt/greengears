from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import Context, loader, RequestContext
from django.middleware.csrf import get_token
from cars.models import Car, Make, Comment, Model, Year, Images
from cars.forms import CarForm, CarSelectForm, CommentForm, CarSelect2, UploadFileForm, StarRatingForm
from django.template import RequestContext
from django.core.context_processors import csrf
from django import http
from cars.uploader import handle_uploaded_file
from django.db.models import F #Ivan
from django.utils import simplejson
from django.db.models import Q
import datetime, math

cars_list = Car.objects.all()

def index(request):
    get_token(request) 
    make_list = Make.objects.all()

    if request.method == "POST":
        selected_make = request.POST['makes']
        selected_model = request.POST['models']
        selected_year = 1 
        
        car = Car.objects.get(MAKE=selected_make, MODEL=selected_model)
        
        return http.HttpResponseRedirect('./' + str(car.id) + '/')
        
    return render_to_response('cars/index.html', {'make_list' : make_list}, RequestContext(request))

def search(request, **args):
    get_token(request) 

    if request.method == "GET":
        output = [] 
        term = request.REQUEST['term']
        if len(term) > 1:
            for car in cars_list:
                name = car.__unicode__()
                if term.lower() in name.lower():
                    output.append({'id':car.id, 'value':name})

        return http.HttpResponse(simplejson.dumps(output), mimetype='application/json')

    if request.method == "POST":
        car = request.POST['carSelected']
        return http.HttpResponseRedirect('/greengears/cars/' + str(car) + '/')
    
def detail(request, id):

    if request.method == 'POST':
        if request.method == "POST":
            form = CarSelectForm(request.POST)
            if form.is_valid():
                carSelected = form.cleaned_data['CarSelected']
                return http.HttpResponseRedirect('./' + str(carSelected) + '/')

    if request.method == 'POST':

        form = CommentForm(request.POST)
        if form.is_valid():
            # create a new item
            contact = Comment.objects.create(
                                       CAR= get_object_or_404(Car, pk=id),
				       NAME = form.cleaned_data['name'],
                                       COMMENT=form.cleaned_data['comment'],
                                       DATE = datetime.datetime.today()
                                       )
            return http.HttpResponseRedirect('./')

    p = get_object_or_404(Car, pk=id)
    car_list = Car.objects.filter(BODYTYPE=p.BODYTYPE).filter( HP__range = (p.HP-25,p.HP+25)).filter( DRIVETRAIN = p.DRIVETRAIN).filter( CURBWEIGHT__range = (p.CURBWEIGHT-500,p.CURBWEIGHT+500)).filter( MPG__range = (p.MPG-5,p.MPG+5)).exclude(id = p.id) #Ivan "Comparable Car" filter
    comments = Comment.objects.filter(CAR=p)
    commentBox = CommentForm(request.POST)
    
    full_stars = int(math.floor(p.RATING.get_rating())) * 2
    empty_stars = 10 - full_stars
    count = p.COUNT - 1
    context = Context({'car' : p, 'comment_list' : comments, 'form' : commentBox, 'car_list' : car_list, 'count':count, 'full_stars' : range(full_stars), 'empty_stars':range(empty_stars)})

    return render_to_response('cars/detail.html', context, context_instance=RequestContext(request))


def edit(request, id):
    p = get_object_or_404(Car, pk=id)
    if request.method == "POST":
        form = CarForm(request.POST)

        if form.is_valid():
            p.MPG = form.cleaned_data['MPG']
            p.HP = form.cleaned_data['HP']
            p.BODYTYPE = form.cleaned_data['BODYTYPE']
            p.TRANSMISSION = form.cleaned_data['TRANSMISSION']
            p.NUM_GEARS = form.cleaned_data['NUM_GEARS']
            p.save()
            return http.HttpResponseRedirect('/cars/')
    else:
        form = CarForm(instance=p)
    context = Context({'title': 'Edit Item', 'form': form, 'car': p })
    return render_to_response('cars/edit.html', context, context_instance=RequestContext(request))

def home(request):
    car_list = Car.objects.all()
    t = loader.get_template('cars/home.html')
    c = Context({
        'car_list': car_list,
    })
    return HttpResponse(t.render(c))

def compare(request, id1, id2):
    p = get_object_or_404(Car, pk=id1)
    k = get_object_or_404(Car, pk=id2)
    count1 = p.COUNT-1
    count2 = k.COUNT-1
    return render_to_response('cars/compare.html', {'car1': p, 'car2': k, 'count1' : count1, 'count2' : count2},
                              context_instance=RequestContext(request))

def upload_file(request, id):
    car = Car.objects.get(pk=id)
    count = car.COUNT - 1
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], car)
            #string = '/home/greengears/media/car_img/' + str(car.YEAR) + '-' + str(car.id) + '-' + str(car.COUNT)
            string = '/media/' + str(car.YEAR) + '-' + str(car.id) + '-' + str(car.COUNT)
            p = Images(CAR_id = id, IMAGE = string)
            p.save()
            car.COUNT = car.COUNT + 1
            car.save()
            return redirect(detail,id)
            #return render_to_response('cars/detail.html/', Context({'id':id}), context_instance=RequestContext(request))
    else:
        form = UploadFileForm()
    return render_to_response('cars/upload.html/', Context({'form': form, 'id':id, 'car':car, 'count':count}), context_instance=RequestContext(request))


def rank(request):
    hp_list = Car.objects.order_by('-HP')[:10]
    weight_list = Car.objects.order_by('CURBWEIGHT')[:10]
    co2_list = Car.objects.order_by('CO2').filter(CO2__gt = 0)[:10]
    co_list = Car.objects.order_by('CO').filter(CO__gt = 0)[:10]
    thc_list = Car.objects.order_by('THC').filter(THC__gt = 0)[:10]
    nox_list = Car.objects.order_by('NOX').filter(NOX__gt = 0)[:10]
    mpg_list = Car.objects.order_by('-MPG')[:10]
    context = Context({'mpg_list' : mpg_list, 'hp_list' : hp_list, 'weight_list' : weight_list, 'co2_list' : co2_list, 'co_list' : co_list, 'thc_list' : thc_list, 'nox_list' : nox_list})
    return render_to_response('cars/rank.html', context, context_instance=RequestContext(request))


def rate(request, id):
    form = StarRatingForm(request.POST)

    if form.is_valid():
        car = Car.objects.get(id=id)
        rating = int(request.REQUEST['star'])       
        
        car.RATING.add(score=rating, user=request.user, ip_address=request.META['REMOTE_ADDR'])
        new_rating = car.RATING.get_rating()
        car.STARS = new_rating
        car.save()
        output = {"rating":new_rating}
        http.HttpResponseRedirect('../')
        return http.HttpResponse(simplejson.dumps(output), mimetype='application/json')

def gallery(request, id):

    if request.method == 'POST':
        if request.method == "POST":
            form = CarSelectForm(request.POST)
            if form.is_valid():
                carSelected = form.cleaned_data['CarSelected']
                return http.HttpResponseRedirect('./' + str(carSelected) + '/')

    p = get_object_or_404(Car, pk=id)
    car_list = Car.objects.filter(BODYTYPE=p.BODYTYPE).filter( HP__range = (p.HP-25,p.HP+25)).filter( DRIVETRAIN = p.DRIVETRAIN).filter( CURBWEIGHT__range = (p.CURBWEIGHT-500,p.CURBWEIGHT+500)).filter( MPG__range = (p.MPG-5,p.MPG+5)).exclude(id = p.id) #Ivan "Comparable Car" filter
    img = Images.objects.filter(CAR = id)
    count = p.COUNT - 1
    context = Context({'car' : p, 'car_list' : car_list, 'count' : count, 'img' : img})
    return render_to_response('cars/gallery.html', context, context_instance=RequestContext(request))

def about(request):
    return render_to_response('cars/about.html', context_instance=RequestContext(request))
