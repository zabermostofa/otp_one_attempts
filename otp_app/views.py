from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from .forms import LoginForm,SignupForm
from django.contrib.auth.models import User
import datetime,random,uuid,calendar
from datetime import datetime , timedelta,date
from django.utils import timezone
from calendar import HTMLCalendar,FRIDAY,SATURDAY,SUNDAY
# Create your views here.

def base(request):
    context = {}
    title = 'base'
    context['title']  = title
    return render(request,f'{title}.html',context)

class Today(HTMLCalendar):
    def __init__(self,year, month ):
        super().__init__(firstweekday=SUNDAY)
        self.year = year 
        self.month = month 
        self.today = date.today()

    def formatday(self, day, weekday):
        if day == 0 :
            return f'<td class="noday"> &nbsp; </td>'
        
        if day == self.today.day and self.month == self.today.month and self.year == self.today.year  :
            return f'<td class="today px-1 bg-warning rounded-circle fw-bolder d-inline-block text-dark"> {day} </td>'
        
        
        
        if weekday == FRIDAY :
            return f'<td class="friday  text-danger fw-bolder"> {day} </td>'
        
        if weekday == SATURDAY :
            return f'<td class="saturday  text-primary fw-bolder"> {day} </td>'
        
        
        return f'<td> {day} </td>'

def home(request):
    context = {}
    title = 'home'
    context['title']  = title

    now = datetime.now()
    context['now']  = now


    month = now.month
    context['month']  = month

    months = list(calendar.month_name)
    context['months']  = months

    month_name = months[month]
    context['month_name']  = month_name

    day = now.day
    context['day']  = day



    year = now.year
    context['year']  = year


    weekday = now.weekday()
    context['weekday']  = weekday

    
    days = list(calendar.day_name)
    context['days']  = days

    day_name = days[weekday]
    context['day_name']  = day_name

    previous_year , previous_month = (year-1,12) if month == 1 else (year,month-1)

    next_year , next_month = (year+1,1) if month == 12 else (year,month+1)

    previous_month_calendar = Today(
        previous_year , previous_month 
    ).formatmonth(
        previous_year , previous_month 
    )
    context['previous_month_calendar']  = previous_month_calendar

    current_month_calendar = Today(
        year , month 
    ).formatmonth(
        year , month 
    )
    context['current_month_calendar']  = current_month_calendar

    next_month_calendar = Today(
        next_year , next_month
    ).formatmonth(
        next_year , next_month
    )
    context['next_month_calendar']  = next_month_calendar

    return render(request,f'{title}.html',context)

def login(request):
    context = {}
    title = 'login'
    context['title']  = title
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(
                request,username = username,
                password = password
            )
            if user :
                if user.last_login:
                    time_difference = timezone.now() - user.last_login

                    if time_difference <= timedelta(minutes=3):

                        auth_login(request,user)
                        messages.success(request,f"{title} successful")
                        return redirect(title)
                    else :
                        otp = random.randint(10,99)
                        otp = str(otp)
                        request.session['username'] = username
                        request.session['otp'] = otp
                        messages.success(request,"logged in more than 3 minutes")
                        messages.info(request,f"your otp is {otp}")
                        return redirect('otp_view')

                else :
                    auth_login(request,user)
                    messages.success(request,"you have logged in for the first time")
                    return redirect(title)

            else:
                messages.error(request,"invalid username or wrong password")
                return redirect(title)


    context['form']  = form
    return render(request,f'{title}.html',context)

def logout(request):
    context = {}
    title = 'logout'
    context['title']  = title
    auth_logout(request)
    return render(request,f'{title}.html',context)

def signup(request):
    context = {}
    title = 'signup'
    context['title']  = title
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            user = authenticate(
                request,username = username,
                password = password1
            )
        
            auth_login(request,user)
            messages.success(request,f"{title} successful")
            return redirect('login')
        else:
            messages.error(request,form.errors)
            return redirect(title)


    context['form']  = form
    return render(request,f'{title}.html',context)

def otp_view(request):
    context = {}
    title = 'otp_view'
    context['title']  = title

    if request.method == 'POST':
        username = request.session.get('username')
        otp_input = request.POST.get('otp')

        if otp_input == request.session['otp']:
            user = get_user_model().objects.get(
                username = username
            )
            auth_login(request,user)
            del request.session['username']
            del request.session['otp']
            messages.success(request,'Correct OTP! login successful')
            return redirect('login')
        
        else :
            request.session.flush()
            messages.error(request,'wrong otp!login again')
            return redirect('login')
        

    return render(request,f'{title}.html',context)

def user_list(request):
    context = {}
    title = 'user_list'
    context['title']  = title
    
    users = User.objects.all()
    context['users']  = users

    return render(request,f'{title}.html',context)