from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth import views as auth_views

from django.http import HttpResponse
from django_pivot.pivot import pivot 
from .filters import FormFilter
from django.db.models import Sum, F, ExpressionWrapper, FloatField,Count
from django.db.models.functions import ExtractMonth, ExtractYear
import json
from django.db.models.functions import TruncMonth

from base.models import Title,YhForm
from .forms import TitForm,FillForm,UserForm,CreateUserForm
from .tables import FormTable
from django.db.models import Q
from datetime import date as dt
from datetime import datetime
import pandas as pd
import numpy as np 
import os
from django.conf import settings
from django.template import *
import json
import csv
from django.forms import formset_factory
#bulit decretor that check if user login he cant go to login/register
# from .decorators import unisauthenticated_user,allowed_users,admin_only


def download_csv(request, queryset):

    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response


def export(request):
    data = download_csv( request, YhForm.objects.filter(username__username='ronen'))
    return HttpResponse (data, content_type='text/csv')
#-----LOG IN -----------------
# @unisauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username').lower()#get data from front
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username) #vheck if there is this user
        except:
            messages.error(request,'User does Not Exitst')
        user = authenticate(request,username=username,password=password)
        if user !=None:
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,'User Or Password does Not Exitst')
    context={}
    return render(request,'base/loginpage.html',context)

#-----LOG OUT -----------------

def logoutUser(request):
    logout(request)
    return redirect('home')

#-----registerUser -----------------
# @unisauthenticated_user
def registerUser(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)#still not commit
            user.username = user.email.lower()#lower case the user
            user.save()
            #defult group employee
            # group = Group.objects.get(name='employee')
            # user.groups.add(group)
            # user_1= form.cleaned_data.get( 'username' )
            # messages.success(request, 'Account was created for '+ user_1)
            # print(request, 'Account was created for '+ user_1)
            login(request,user)#login the user
            return redirect('home')
        else:
            messages.error(request,'Error accor during regstrition')
    context={'form':form,} 
    return render(request,'base/registerpage.html',context)
    
#----------UPDATE TITLE  ------------
@login_required(login_url='login')
# @admin_only
def up(request):
    forms = YhForm.objects.all()
    titles = Title.objects.all()
    total_tit = Title.objects.all().count()

    context = {'titles':titles,'total_tit':total_tit,'forms':forms
               }
    return render (request,'base/up.html',context)

#----------CREATE TITLW ------------      
@login_required(login_url='login')

# @admin_only
def createTit(request):
    form=TitForm
    
    if request.method == 'POST':
        form = TitForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('tit-page')
    context={'form':form}
    return  render(request,'base/create_tit.html',context)

#----------UPDATE TITLW ------------ 
    
@login_required(login_url='login')
# @admin_only
def updateTit(request,pk):
    tit = Title.objects.get(id=pk)
    form = TitForm(instance=tit)
    if request.method == 'POST':
        form = TitForm(request.POST,instance=tit)
        if form.is_valid():
            form.save()
            return redirect('tit-page')
    context = {'form':form,'tit':tit}
    return render(request,'base/create_tit.html',context)

#----------DELETE TITLW ------------ 
    
@login_required(login_url='login')
# @admin_only
def deleteTit(request,pk):
    tit = Title.objects.get(id=pk)
    if request.method == 'POST':
        tit.delete()
        return redirect('tit-page')
    context={'obj':tit}
    return  render(request,'base/delete.html',context)

#----------CREATE FORM ------------     
@login_required(login_url='login')
def createForm(request):
    user = request.user
    gl=''
    dm=''
    if  request.user.get_username()=="ronen" :
        gl='Ronen'
        dm='Ronen'
    FillFormSet = formset_factory(FillForm, extra=2, can_delete=True)  # Change extra to 1 and set can_delete to True

    forms=YhForm.objects.filter(username=user).order_by('-created')[:5]
    above=YhForm.objects.values('username__username','date').annotate(Sum('percent')).filter(username=user).order_by('-date')[:5]
    formset = FillFormSet(form_kwargs={'user': request.user})
    if user=='ronen':
        print(user)
    if request.method == 'POST':
        formset = FillFormSet(request.POST, form_kwargs={'user': request.user})
        if formset.is_valid():
            for form in formset:
                if not form.cleaned_data.get('DELETE'):  # Check if the DELETE checkbox is not checked
                    fill = form.save(commit=False)
                    fill.username = request.user
                    fill.gl = gl.lower()
                    fill.dm = dm.lower()
                    fill.save()
            return redirect('create-form')
    current_datetime = datetime.now()
    user1=request.user
    if user1 :
        user = User.objects.get(username=user1)
        last_login = user.last_login
    context = {'formset': formset, 'forms': forms, 'above': above, 'last_login': last_login, 'current_datetime': current_datetime}
    return  render(request,'base/fillform.html',context)

    
#----------UPDATE FORM ------------     
@login_required(login_url='login')
def updateForm(request, pk):
    user = request.user
    yh_form = YhForm.objects.get(id=pk)
    form = FillForm(instance=yh_form, user=request.user)
    forms=YhForm.objects.filter(username=user).order_by('-created')[:5]
    # If the user is not the owner of the form, they can't edit it
    if request.user != yh_form.username:
        return HttpResponse('<h1>You cannot be here !!!</h1>')

    if request.method == 'POST':
        form = FillForm(request.POST, instance=yh_form, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form, 'yh_form': yh_form, 'update': True,'forms':forms}
    return render(request, 'base/fillform.html', context)
    
#----------DELETE FORM ------------      
@login_required(login_url='login')
def deleteForm(request,pk):
    for1 = YhForm.objects.get(id=pk)
        #if the user is not the owner of the form he caant edit it
    if request.user !=for1.username:
        return HttpResponse('<h1>You can be here !!!</h1>')
    if request.method == 'POST':
        for1.delete()
        return redirect('home')
    context={'obj':for1}
    return  render(request,'base/delete.html',context)

#----------userProfile ------------     
@login_required(login_url='login')
def userProfile(request,pk):
    user = User.objects.get(id=pk)
    fillforms=user.yhform_set.all()
    forms=user.yhform_set.all()

    tit = Title.objects.all()
    context={'user':user,'fillforms':fillforms,'tit':tit,'forms':forms}
    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def updateUser(request):
    user=request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form=UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile',pk=user.id)
    context = {'form':form}
    return render(request,'base/update_user.html',context)

@login_required(login_url='login')
# @admin_only
def titPage(request):
    if request.GET.get('q')!= None: 
        q=request.GET.get('q')
    else:
        q=""
    titles = Title.objects.filter(
        Q(name__icontains = q) 
       ).order_by("-created")
    
    
    current_datetime = datetime.now()
    user1=request.user
    if user1 :
        user = User.objects.get(username=user1)
        last_login = user.last_login
    context = {'titles':titles,'current_datetime':current_datetime,'last_login':last_login}
    return render(request,'base/titpage.html',context)

#----------HOME ------------
@login_required(login_url='login')
def home(request):
    a= request.path 
    if a=='/':
        a='Home'
    user = request.user

    titles = Title.objects.all()
    forms=YhForm.objects.filter(username=request.user).order_by('-date')
    formfilter=FormFilter(request.GET ,queryset=forms)
    forms=formfilter.qs

    above=YhForm.objects.values('username__username','date').annotate(Sum('percent')).filter(username=request.user).order_by('-percent__sum')
    abovefilter=FormFilter(request.GET ,queryset=above)
    above=abovefilter.qs
    # q = request.GET.get('q') if request.GET.get('q') != None else ''
    # print(q)
    # forms = YhForm.objects.filter(
    #     Q(title__name__icontains = q) 
    #    ) #icontains no case sansitive -->contains is case sanstiv
    # forms = YhForm.objects.filter(Q(title__name__icontains=q))
    current_datetime = datetime.now()
    user1=request.user
    if user1 :
        user = User.objects.get(username=user1)
        last_login = user.last_login
    if  'csv' in request.method.POST:
        data = download_csv(request, forms)
        return HttpResponse (data, content_type='text/csv')
        
    context = {'titles':titles,'forms':forms,'above':above,
    # 'below':below,
    'formfilter':formfilter,
    'current_datetime':current_datetime,'last_login':last_login,'a':a,
    }
    return render (request,'base/home.html',context)
#----------------------------------------------------------

@login_required(login_url='login')
def userDashboard(request):
    a= request.path 
    print(a)
    user = request.user

    titles = Title.objects.all()
    forms=YhForm.objects.filter(username=user).order_by('-date')
    formfilter=FormFilter(request.GET ,queryset=forms)
    forms=formfilter.qs

    above=YhForm.objects.values('username__username','date').annotate(Sum('percent')).filter(username=user).order_by('-percent__sum')
    abovefilter=FormFilter(request.GET ,queryset=above)
    above=abovefilter.qs

    # below=YhForm.objects.values('username__username','date').annotate(Sum('percent')).filter(percent__sum__lt=100,username=user) .order_by('-date')
    # belowfilter=FormFilter(request.GET ,queryset=below)
    # below=belowfilter.qs

    current_datetime = datetime.now()
   
    # Calculate average percent for each month without Friday and Saturday
    monthly_averages = {}
    for form in forms:
        if form.date.weekday() not in [4, 5]:
            month_year = form.date.strftime('%B %Y')
            if month_year not in monthly_averages:
                monthly_averages[month_year] = []
            monthly_averages[month_year].append(form.percent)
    for month in monthly_averages:
        monthly_averages[month] =round(sum(monthly_averages[month]) / len(monthly_averages[month]), 2)
    user1=request.user
    if user1 :
        user = User.objects.get(username=user1)
        last_login = user.last_login

    if  request.method=='POST':
        data = download_csv(request, forms)
        return HttpResponse (data, content_type='text/csv')    
    context = {
    'titles':titles,
    'forms':forms,
    'above':above,
    'formfilter':formfilter,
    'last_login':last_login,
    'current_datetime':current_datetime,
    'monthly_averages': monthly_averages, 
    'a':a,} 
    return render (request,'base/userdashboard.html',context)
#----------------------------------------------------------

@login_required(login_url='login')
def userDashboard_m(request):
    a= request.path 
    user = request.user
    this_month = datetime.now().month
   

    titles = Title.objects.all()

    forms=YhForm.objects.filter(username=user,date__month=this_month).order_by('-date')
    formfilter=FormFilter(request.GET ,queryset=forms)
    forms=formfilter.qs

    above=YhForm.objects.values('username__username','date').annotate(Sum('percent')).filter(username=user,date__month=this_month,) .order_by('-date')
    abovefilter=FormFilter(request.GET ,queryset=above)
    above=abovefilter.qs

    below=YhForm.objects.values('username__username','date').annotate(Sum('percent')).filter(username=user,date__month=this_month,) .order_by('-date')
    belowfilter=FormFilter(request.GET ,queryset=below)
    below=belowfilter.qs
    current_datetime = datetime.now()
    user1=request.user
    if user1 :
        user = User.objects.get(username=user1)
        last_login = user.last_login
    if  request.method=='POST':
        data = download_csv(request, forms)
        return HttpResponse (data, content_type='text/csv') 
  
    context = {'titles':titles,'forms':forms,'above':above,'below':below,
    'formfilter':formfilter,'a':a,
    'current_datetime':current_datetime,'last_login':last_login
    }
    return render (request,'base/userdashboard_m.html',context)
    #----------------------------------------------------------
@login_required(login_url='login')
# @admin_only
def mangerDashboard(request):
    # for p in YhForm.objects.raw('SELECT * FROM base_yhform'):
    #    print(p.date)

    # for p in people:
    #    print(p)
    
    a= request.path 
    user = request.user

    titles = Title.objects.all()
    forms=YhForm.objects.filter().order_by('-date')
    formfilter=FormFilter(request.GET ,queryset=forms)
    forms=formfilter.qs

    above=YhForm.objects.values('username__username','date').annotate(Sum('percent')).order_by('-percent__sum')
    abovefilter=FormFilter(request.GET ,queryset=above)
    above=abovefilter.qs

    qs = YhForm.objects.all().values("username__email", "date", "percent")
    tp=pivot(qs,"username__email", "date", "percent")
    table = FormTable(YhForm.objects.all(),template_name="django_tables2/semantic.html")
   

    data = pd.DataFrame(qs)
    data = data.fillna(0)

   
    current_datetime = datetime.now()
    user1=request.user
    if user1 :
        user = User.objects.get(username=user1)
        last_login = user.last_login
    if  request.method=='POST':
        data = download_csv(request, forms)
        return HttpResponse (data, content_type='text/csv') 
    context = {
    'titles':titles,
    'forms':forms,
    'above':above,
    'tp':tp,
    'formfilter':formfilter,
    'current_datetime':current_datetime,
    'last_login':last_login,
    'a':a,
  
    'table':table,
    }
    return render (request,'base/mangerdashboard.html',context)

@login_required(login_url='login')
# @admin_only
def mangerDashboard_m(request):
    # for p in YhForm.objects.raw('SELECT * FROM base_yhform'):
    #    print(p.date)

    # for p in people:
    #    print(p)
    this_month = datetime.now().month
    a= request.path 
    user = request.user

    titles = Title.objects.all()
    forms=YhForm.objects.filter(date__month=this_month).order_by('-date')
    formfilter=FormFilter(request.GET ,queryset=forms)
    forms=formfilter.qs

    above=YhForm.objects.values('username__username','date').annotate(Sum('percent')).filter(date__month=this_month,) .order_by('-date')
    abovefilter=FormFilter(request.GET ,queryset=above)
    above=abovefilter.qs

    qs = YhForm.objects.filter(date__month=this_month).values("username__email", "date", "percent")
    tp=pivot(qs,"username__email", "date", "percent")
    table = FormTable(YhForm.objects.all(),template_name="django_tables2/semantic.html")
    print(table)

    data = pd.DataFrame(qs)
    data = data.fillna(0)
   
 
 
    # displaying the DataFrame
 
    
  
    current_datetime = datetime.now()
    user1=request.user
    if user1 :
        user = User.objects.get(username=user1)
        last_login = user.last_login
    if  request.method=='POST':
        data = download_csv(request, forms)
        return HttpResponse (data, content_type='text/csv') 
    context = {
    'titles':titles,
    'forms':forms,
    'above':above,
    'tp':tp,
    'formfilter':formfilter,
    'current_datetime':current_datetime,
    'last_login':last_login,
    'a':a,

    'table':table,
    }
    return render (request,'base/mangerdashboard_m.html',context)

def color_negative_red(val):
    if val < 100:
        color = 'orange' 
    elif  val > 100:
        color = 'red'
    else:
        color = 'green'
    return 'color: % s' % color


@login_required(login_url='login')
# @admin_only
def dmdashboard(request):
    a= request.path 
    user = request.user

    titles = Title.objects.all()
    forms=YhForm.objects.all().order_by('-date')
    formfilter=FormFilter(request.GET ,queryset=forms)
    forms=formfilter.qs

    above=YhForm.objects.values('username__username','date',"gl","dm").annotate(Sum('percent')).order_by('-percent__sum')
    abovefilter=FormFilter(request.GET ,queryset=above)
    above=abovefilter.qs

    qs = YhForm.objects.all().values("username__email", "date", "percent")
    tp=pivot(qs,"username__email", "date","gl")
    table = FormTable(YhForm.objects.all(),template_name="django_tables2/semantic.html")
   

    data = pd.DataFrame(qs)
    data = data.fillna(0)
 

   
    current_datetime = datetime.now()
    user1=request.user
    if user1 :
        user = User.objects.get(username=user1)
        last_login = user.last_login
    if  request.method=='POST':
        data = download_csv(request, forms)
        return HttpResponse (data, content_type='text/csv') 
    monthly_data = YhForm.objects.annotate(
        month=ExtractMonth('date'),
        year=ExtractYear('date')
    ).values('username__username', 'title__name', 'month', 'year').annotate(
        total_percent=Sum('percent')
    )

    monthly_user_total = YhForm.objects.annotate(
        month=ExtractMonth('date'),
        year=ExtractYear('date')
    ).values('username__username', 'month', 'year').annotate(
        user_monthly_total=Sum('percent')
    )

    filtered_monthly_data = FormFilter(request.GET, queryset=monthly_data).qs
    filtered_monthly_user_total = FormFilter(request.GET, queryset=monthly_user_total).qs

    monthly_data_with_user_totals = []

    for item in filtered_monthly_data:
        for user_total in filtered_monthly_user_total:
            if (item['username__username'] == user_total['username__username'] and
                item['month'] == user_total['month'] and
                item['year'] == user_total['year']):
                item['user_title_percent'] = item['total_percent'] / user_total['user_monthly_total']
                monthly_data_with_user_totals.append(item)
                break
    context = {
    'titles':titles,
    'forms':forms,
    'above':above,
    'tp':tp,
    'formfilter':formfilter,
    'current_datetime':current_datetime,
    'last_login':last_login,
    'a':a,
    'table':table,
     'monthly_data': monthly_data_with_user_totals,
    }
    return render (request,'base/dmdashboard.html',context)




@login_required(login_url='login')
def index(request):
    context = {}
    return render (request,'base/index.html',context) 

@login_required(login_url='login')
def charts(request):
    a= request.path 
    user = request.user
    forms=YhForm.objects.filter().order_by('-date')
    formfilter=FormFilter(request.GET ,queryset=forms)
    forms=formfilter.qs

    above=YhForm.objects.values('username__username','date').annotate(Sum('percent')).order_by('-percent__sum')
    abovefilter=FormFilter(request.GET ,queryset=above)
    above=abovefilter.qs
    #line charts
    labels1 = []
    data1 = []
    queryset1=YhForm.objects.values('username__username','date').annotate(Sum('percent')).order_by('-date')
    queryset1filter=FormFilter(request.GET ,queryset=queryset1)
    queryset1=queryset1filter.qs
    for date in queryset1: 
        labels1.append(date['date'])
        data1.append(date['percent__sum'])
    #---------------------------------------------   
    #Bar charts
    labels = []
    data = []
    queryset = YhForm.objects.values('username__username','date').annotate(Sum('percent')).filter(username=user).order_by('date')
    querysetfilter=FormFilter(request.GET ,queryset=queryset)
    queryset=querysetfilter.qs
    for dep in queryset:
        labels.append(dep['date'])
        data.append(dep['percent__sum'])
    #---------------------------------------------  
    current_datetime = datetime.now()
    user1=request.user
    if user1 :
        user = User.objects.get(username=user1)
        last_login = user.last_login
    context = {'labels': labels,
                'data': data,
                'labels1': labels1,
                'data1': data1,
                'a':a,
                'forms':forms,
                'formfilter':formfilter,
                'current_datetime':current_datetime,
                'last_login':last_login
                }
    return render (request,'base/charts-chartjs.html',context) 


def calculate_percentages_by_month():
    # Get distinct users and titles
    distinct_users = User.objects.all()
    distinct_titles = Title.objects.all()

    # Initialize an empty list to store the results
    results = []

    # Loop through each user and title combination
    for user in distinct_users:
        for title in distinct_titles:
            # Calculate the sum of percent for the current user and title grouped by month
            monthly_data = YhForm.objects.filter(username=user, title=title).annotate(month=TruncMonth('date')).values('month').annotate(sum_percent=Sum('percent')).order_by('month')

            for month_data in monthly_data:
                # Calculate the total sum of percent for the current user and title for each month
                total_sum_percent = YhForm.objects.filter(username=user, date__month=month_data['month'].month, date__year=month_data['month'].year).aggregate(Sum('percent'))['percent__sum']

                if month_data['sum_percent'] is not None and total_sum_percent is not None and total_sum_percent != 0:
                    # Calculate the required value
                    calculated_value = month_data['sum_percent'] / total_sum_percent

                    # Append the result to the list
                    results.append({
                        'user': user,
                        'title': title,
                        'month': month_data['month'],
                        'calculated_value': calculated_value
                    })

    return results