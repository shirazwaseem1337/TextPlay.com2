#This is the file I created

from cgitb import text
from email import message
from http.client import HTTPResponse;
from os import remove;
from unicodedata import name;
from Home.models import Contact;
from datetime import datetime;
from os import remove;
from django.http import HttpResponse;
from django.shortcuts import render,redirect;
from django.forms import inlineformset_factory;
from django.contrib.auth.forms import UserCreationForm;
from .forms import CreateUserForm;
from django.contrib import messages;
from django.http import HttpResponse
from django.shortcuts import render,HttpResponse;
from django.contrib.auth import authenticate,login,logout;
from django.contrib.auth.decorators import login_required



def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        # user get saved in database (admin) 
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()

                user=form.cleaned_data.get('username')
                messages.success(request, 'Account is created for '+user)
                return redirect('login')

        context = {'form':form}
        return render(request,'register.html',context)



def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect('index')
                # Pass the views name 

            else:
                messages.info(request, 'Username or Password is incorrect.')


        context = {}
        return render(request,'login.html',context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):
    # params={'name':'shiraz','age':17}
    return render(request,'index.html')


@login_required(login_url='login')
def analyze(request):
    djtext= request.POST.get('text','default')
    removepunc= request.POST.get('punctuationremoved','off') 
    captext=request.POST.get('capitalize','off')
    lineremover=request.POST.get('lineremover','off')
    extraspaceremover=request.POST.get('spaceremover','off')
    lowercase=request.POST.get('lowercasetext','off')
    textlengthwithoutspace=request.POST.get('textlengthwithoutspace','off')
    textlengthwithspace=request.POST.get('textlengthwithspace','off')

    print(djtext)
    

    # For removing punctuations
    if (removepunc=="on"):
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        analyzed = ""
        for char in djtext:
            if char not in punctuations:
                analyzed=analyzed+char
    

        params={'purpose': "Removing Punctuations", 'analyzed_text': analyzed}
        djtext=analyzed
        # return render(request,'analyze.html',params)



    #for capitalizing the text
    if (captext=="on"):
        analyzed=""
        for char in djtext:
            analyzed=analyzed+char.upper()

        params={'purpose': "Capitalaizing text", 'analyzed_text': analyzed}
        djtext=analyzed
        # return render(request,'analyze.html',params)

    #for removing the space between lines
    if (lineremover=="on"):
        analyzed=""
        for char in djtext:
            if char !="\r" and char != "\n":
                analyzed=analyzed+char
        params={'purpose': "Line remover", 'analyzed_text': analyzed}
        djtext=analyzed
        # return render(request,'analyze.html',params)

        # For removing the space between the text
    if (extraspaceremover=='on'):
        analyzed=""
        for index,char in enumerate(djtext):
            if djtext[index] == " " and djtext[index+1]==" ":
                pass
            else:
                analyzed=analyzed+char
        params={'purpose': "Extra Space remover", 'analyzed_text': analyzed}

    if (lowercase=='on'):
        analyzed=""
        for char in djtext:
            analyzed=analyzed+char.lower()
        params={'purpose': "Lower case text", 'analyzed_text': analyzed}
        
    if (textlengthwithoutspace=='on'):
        analyzed=""
        for char in djtext.split(" "):
            analyzed=analyzed+char
        params={'purpose': "Length of text without space", 'analyzed_text': len(analyzed)}

    if (textlengthwithspace=='on'):
        analyzed=""
        for char in djtext:
            analyzed=analyzed+char
        params={'purpose': "Length of text with space", 'analyzed_text': len(analyzed)}


    if(removepunc!='on' and extraspaceremover!='on' and lineremover!='on' and captext!='on' and lowercase!='on' and textlengthwithoutspace!='on' and textlengthwithspace!='on'):
        return HttpResponse('Please enable any one of the options')

    return render(request,'analyze.html',params)


@login_required(login_url='login')

def contact(request):

    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        desc=request.POST.get('desc')
        contact=Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, name + ', your form has been successfully submitted..')

 
    return render(request,'contact.html')