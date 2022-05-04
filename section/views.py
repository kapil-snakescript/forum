from multiprocessing import context
from django.shortcuts import redirect, render
from django.utils import timezone
from .models import Section,NewPost
from .forms import AddSectionForm
from django.contrib import messages
from django.core.paginator import Paginator

def home(request):
    if not request.user.is_authenticated:
        return redirect('login-user')

    sections = Section.objects.all().order_by('-id')

    if request.method == "GET" and request.GET.get('query'):
        sections = Section.objects.filter(title__icontains = request.GET.get('query')).order_by('-id')

    if request.method == "POST" and request.POST.get('topic_select'):
        sections = Section.objects.filter(topic = request.POST.get('topic_select')).order_by('-id')

        

    page_number = request.GET.get('page')
    context = {}
    paginator = Paginator(sections, per_page=4)
    
    try:
        paginated_data = paginator.get_page(page_number)  # returns the desired page object
    except:
        # if page_number is not an integer then assign the first page
        paginated_data = paginator.page(1)



    context['paginated_data'] = paginated_data
    try:
        context['next_page'] = paginated_data.next_page_number()
    except:
        pass
    context['has_next']=paginated_data.has_next()
    context['sections']=sections
    context['paginator']=paginator
    ##Topic dropdown
    topics = []
    topic = Section.objects.all()
    for topic in topic:
        if topic.topic not in topics:
            topics.append(topic.topic)
    context['topic'] = topics
    return render(request,'section/home.html',context)


def add_section(request):
    if not request.user.is_superuser:
        messages.info(request,"You dont have permission to create section")
        return redirect('/')

    if request.method == 'POST':
        form = AddSectionForm(request.POST,pk=None)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            topic = cleaned_data.get("topic")
            title = cleaned_data.get("title")
            description = cleaned_data.get("description")
            
            section = Section.objects.create(
                topic=topic,
                title=title,
                description = description,
                user = request.user
            )
            if section:
                return redirect('section-list')
    else:
        form = AddSectionForm(pk=None)


    context = {
        'form':form
    }
    return render(request,'section/addsection.html',context)


def edit_section(request,pk):
    if not (request.user.is_superuser or request.user.is_moderator) :
        messages.info(request,"You dont have permission to edit section")
        return redirect('/')

    
    section = Section.objects.filter(id=pk).last()
    if not section:
        messages.info(request,"Section you are trying to edit not exists!")
        return redirect('/')

    if request.method == 'POST':
       
        form = AddSectionForm(request.POST,pk=pk)
        if form.is_valid():
            
            cleaned_data = form.cleaned_data
            topic = cleaned_data.get("topic")
            title = cleaned_data.get("title")
            description = cleaned_data.get("description")
            section.title = title
            section.topic = topic
            section.description = description
            section.update_by = request.user
            section.save()
            messages.info(request,"Section edit successfully!")
            return redirect('section-list')
        
    else:
        form = AddSectionForm(pk=pk)

    context = {
        'form':form,
        'section':section
        }
    return render(request,'section/addsection.html',context)


def delete_section(request,pk):
    if not request.user.is_superuser:
        messages.info(request,"You don't have permission to delete section!")
        return redirect('/')
    else:
        if Section.objects.filter(id=pk).exists():
            Section.objects.filter(id=pk).delete()
            messages.info(request,"Section Deleted seccessfully")
        else:
            messages.info(request,"Section you are trying to delete not exists!")
    return redirect('/')
    



def post_list(request, section_id):
    context = {}
    if request.method == "POST":
        post = request.POST.get("post")
        obj = Section.objects.get(id=section_id)
        NewPost.objects.create(creator = request.user,post=post,section=obj)

    section = Section.objects.get(id=section_id)
    posts = section.newpost_set.all()

    page_number = request.GET.get('page')
    paginator = Paginator(posts, per_page=3)

    try:
        paginated_data = paginator.get_page(page_number)  # returns the desired page object
    except:
        # if page_number is not an integer then assign the first page
        paginated_data = paginator.page(1)

    context['paginated_data']=paginated_data
    context['paginator'] = paginator
    try:
        context['next_page'] = paginated_data.next_page_number()
    except:
        pass
    context['has_next']=paginated_data.has_next()


    context['posts'] = posts
    context['section'] = section
    return render(request, "section/postlist.html", context)