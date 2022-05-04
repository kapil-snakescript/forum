from multiprocessing import context
from telnetlib import AUTHENTICATION
from django.shortcuts import render,HttpResponseRedirect,redirect
from django.views import View
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import authenticate, login as loginuser,logout as _logout
from .forms import EditProfileForm
from datetime import timedelta, date
from django.core.paginator import Paginator
# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('section-list')
    if request.method=='POST':
        # print(request.POST.values, 'requestdata check')
        full_name=request.POST['fullname']
        username=request.POST['username']
        password=make_password(request.POST['password'])

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request,'registration.html',{'error':'Username already exists'})
        
        user=User.objects.create(full_name=full_name,username=username,password=password)
        user.save()
        return redirect('login-user')
    return render(request,'registration.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('section-list')
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                loginuser(request,user)
                return redirect('section-list')
                
        else:
            messages.error(request, 'Invalid username or password')
            return render(request,'login.html',{'error':'Invalid username or password'})
    return render(request,'login.html')

        
def user_list(request):
    if not request.user.is_authenticated:
        return redirect('login-user')
    if not (request.user.is_superuser or request.user.is_moderator):
        messages.info(request,"You dont have permission to see users list")
        return redirect("/")
    users = User.objects.exclude(id=request.user.id)

    page_number = request.GET.get('page')
    context = {}
    paginator = Paginator(users, per_page=4)

    try:
        paginated_data = paginator.get_page(page_number)  # returns the desired page object
    except:
        # if page_number is not an integer then assign the first page
        paginated_data = paginator.page(1)

    context['users']=users
    context['paginated_data']=paginated_data
    context['paginator'] = paginator
    try:
        context['next_page'] = paginated_data.next_page_number()
    except:
        pass
    context['has_next']=paginated_data.has_next()
    return render(request,'registration/users.html',context)


def my_profile(request):
    
    if not request.user.is_authenticated:
        messages.info(request,"You need to login to see your profile!")
        return redirect("/")

    return render(request,'registration/profile.html')

def logout(request):
    _logout(request)
    return redirect('/')



def edit_profile(request):
    user = User.objects.filter(id=request.user.id).first()
    pk=user.id
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST,pk=pk)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            fullname = cleaned_data.get("fullname")
            username = cleaned_data.get("username")
            user.full_name = fullname
            user.username = username
            user.save()
            messages.info(request,"Profile Edit successfully!")
            return redirect('my-profile')
    else:
        form = EditProfileForm(pk=pk)
        

    context = {
                'form':form, 
                'user':user,
                }
    return render(request,'registration/editprofile.html',context)




def edit_user(request,pk):
    if not (request.user.is_superuser or request.user.is_moderator):
        messages.info(request,"You dont have permissions to edit user!")
        return redirect("/")
    user = User.objects.filter(id=pk).first()
    if user.ban_till_date:
        if  user.ban_till_date<date.today():
            user.ban_till_date = None
            user.save()
    if request.method == 'POST':
        role = request.POST.get("role")
        print(role)
        is_ban = request.POST.get("ban_permanent")
        ban_days= request.POST.get("days")
        if role == "1":
            user.is_superuser = False
            user.is_moderator = False
        elif role == "2":
            user.is_superuser = False
            user.is_moderator = True
        elif role == "3":
            user.is_superuser = True
            user.is_moderator = False
        if is_ban:
            user.is_baned_permanent = True
        else:
            user.is_baned_permanent = False
        if ban_days:
            if int(ban_days)>0:
                user.ban_till_date  = date.today() + timedelta(days=int(ban_days))
        user.save()
            
    context = {
                'user':user,
                 }

    return render(request,'registration/edituser.html',context)