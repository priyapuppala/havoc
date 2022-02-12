from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.core.mail import EmailMessage
from django.conf import settings
from django.db.models import Q
from entreprenuer.models import EntreprenuerIdeas


def home(request):
    name = request.session['name']
    return render(request, 'ihome.html', {'name': name})


def logout(request):
    del request.session['name']
    del request.session['email']
    return redirect('/home')


def profile(request):
    if request.method == 'POST':
        form = InvestorProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form1 = form.save(commit=False)
            email = request.session['email']
            form1.fullname = Investor.objects.values_list('fullname', flat=True).get(email=email)
            form1.email = email
            form1.location = Investor.objects.values_list('location', flat=True).get(email=email)
            form1.mobile = Investor.objects.values_list('mobileno', flat=True).get(email=email)
            form1.save()
            del request.session['email']
            return redirect('/investor/login')
    else:
        form = InvestorProfileForm
    return render(request, 'iprofile.html', {'form': form})


def details(request, ideaname):
    eni = EntreprenuerIdeas.objects.get(ideaname=ideaname) # select * from investors
    request.session['ideaname'] = ideaname
    return render(request, 'idetails.html', {'eni': eni})


def services(request):  # normal page
    return render(request, 'iservices.html')


def about(request):  # normal page
    return render(request, 'iabout.html')


def content(request):  # startup requests
    email = request.session['email']
    enpideas = EntreprenuerIdeas.objects.filter(invmail=email)
    enpideasall = EntreprenuerIdeas.objects.all()
    inv = InvestorProfile.objects.filter(email='a@a.com')  # select * from investors
    return render(request, 'icontent.html', {'inv': inv, 'enpideas': enpideas, 'enpideasall': enpideasall})


def appointment(request,enpmail):  # startup after approval form
    if request.method == 'POST':
        form = InvestorApprovalForm(request.POST)
        if form.is_valid():
            atime = form.data['atime']
            adate = form.data['adate']
            feedback = form.data['feedback']
            subject = 'Appointment Regarding The Posted Start Up Idea '+ request.session['ideaname'] +' in the HAVOC From '+ request.session['name']
            invdet = 'My name is ' + request.session['name'] + '. I am a Investor and I am very happy about to check your StartUp Idea and I really want to give a shot at it. I hope our meeting goes well.'
            mess = invdet+'\n\nTime Of The Appointment : ' + atime + '\nDate Of The Appointment : ' + adate + '\nAbout Your StartUp Idea\n' +feedback + '\nAll The Best From Havoc'
            email = EmailMessage(subject,mess, to=[enpmail])
            email.send()
            EntreprenuerIdeas.objects.filter(ideaname=request.session['ideaname']).update(invmail='havoc@gmail.com')
            return redirect('/investor/successful')
    return render(request, 'iappointment.html')


def ignore(request,enpmail):
    idea = request.session['ideaname']
    inv = EntreprenuerIdeas.objects.values_list('invmail', flat=True).get(ideaname=idea)
    if inv==request.session['email']:
        EntreprenuerIdeas.objects.filter(ideaname=idea).update(invmail='havoc@gmail.com')
        subject = 'Sorry For StartUp Idea '+request.session['ideaname']+' Rejection'
        mess = 'Your StartUp Idea Posted in Havoc to is rejected by the '+ request.session['name']+'\nBut do not let your confidence down still your idea is visible to remaining investors.'
        email = EmailMessage(subject,mess, to=[enpmail])
        email.send()
    return redirect('/investor/content')


def successful(request):  # continue to requests page form
    return render(request, 'isuccessful.html')


def registerlogin(request):
    if request.method == 'POST':
        if request.POST.get('submit') == 'login':
            form = InvestorLoginForm(request.POST)
            if form.is_valid():
                email = form.data["email"]
                pwd = form.data["password"]
                if email == 'admin@gmail.com' and pwd == 'admin':
                    return redirect('/havocadmin/home')
                flag = Investor.objects.filter(Q(email__iexact=email) & Q(password__iexact=pwd))
                if flag:
                    request.session['email'] = email
                    inv = Investor.objects.values_list('fullname', flat=True).get(email=email)
                    request.session['name'] = inv
                    return redirect('/investor/home')
                else:
                    form = InvestorForm
                    return render(request, 'i-login.html', {'form': form})
        elif request.POST.get('submit') == 'register':
            form = InvestorForm(request.POST)
            if form.is_valid():
                form.save()
                request.session['email'] = form.cleaned_data.get('email')
                return redirect('/investor/profile')
    else:
        form = InvestorForm
    return render(request, 'i-login.html', {'form': form})


def contact(request):
    if request.method == 'POST':
        form = InvestorContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/investor/home')
    else:
        form = InvestorContactForm
    return render(request, 'icontact.html', {'form': form})
