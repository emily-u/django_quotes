from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request,'quotes/index.html')

def regis(request):
    result = User.objects.regis_validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/main')
    
    request.session['user_id'] = result.id
    messages.error(request, "Successfully registered!")
    return redirect('/quotes')

def login(request):
    result = User.objects.login_validator(request.POST)
    if not result:
        messages.error(request, "login info invalid")
        return redirect('/main')
    else:
        request.session['user_id'] = result.id
        messages.error(request, "Successfully logged in!")
        return redirect('/quotes')

def logout(request):
    request.session.clear()
    return redirect('/main')

def addquotes(request):
    errors = []
    if len(request.POST['quotedby']) < 3:
        errors.append("Quoted by: more than 3 characters")
    if len(request.POST['quotes']) < 10:
        errors.append("Message: more than 10 characters")
        
    for error in errors:
        messages.error(request, error)
        return redirect('/quotes')

    else:
        Quote.objects.create(content=request.POST["quotes"],author=request.POST["quotedby"],uploader=User.objects.get(id=request.session['user_id']))
        return redirect('/quotes')

def addlists(request):
    if request.method:
        Quote.objects.get(id=request.POST['quote_id']).liked_by.add(User.objects.get(id=request.session['user_id']))

        # Quote.objects.exclude(id=request.POST['quote_id']).all()

        return redirect('/quotes')

def quotes(request):
    try:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'unlike_quotes':Quote.objects.exclude(liked_by=request.session['user_id']),
            'favorite':User.objects.get(id=request.session['user_id']).favorite.all()
        }
        return render(request,'quotes/result.html',context)

    except KeyError:
        return redirect('/main')
    
def relists(request):
    if request.method:
        User.objects.get(id=request.session['user_id']).favorite.remove(Quote.objects.get(id=request.POST['quote_id']))
        return redirect('/quotes')

def showuser(request,user_id):
    thoseusers = User.objects.get(id=user_id)
    thoseitems = thoseusers.uploaded_quotes.all()
    context = {
        'showuser': thoseusers,
        'showitem': thoseitems,
        "len": len(thoseitems)
    }
    return render(request,'quotes/user.html',context)