from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from .models import otp_user, Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from users.models import User
from django.views.generic import ListView, CreateView, DetailView, DeleteView, FormView, RedirectView, TemplateView, UpdateView, View
from .froms import SearchForms
from django.db.models import Q
# from kavenegar import KavenegarAPI
from random import randint
from django.utils import timezone


def home_(request):
    Searchform = SearchForms(request.POST)

    if request.method == "POST":
        if Searchform.is_valid():
            title = Searchform.cleaned_data['title']
            content = Searchform.cleaned_data['content']
            author = Searchform.cleaned_data['author']

            if Searchform.cleaned_data['active']:
                active = True
            else:
                active = False
            resposne = Post.objects.filter(Q(content__contains=content) & Q(active=active) & Q(author__username__startswith=author))
        else:
            resposne = Post.objects.all()
    else:
        resposne = Post.objects.all()
    context = {
        'searchform':Searchform,
        'context':resposne
    }
    return render(request, 'post/home.html', context)


def home(request):
    if request.method == 'POST':
        searchTitle = request.POST.get('title')
        searchcontent = request.POST.get('content')
        searchauthor = request.POST.get('author')
        publish_time_hieght = request.POST.get('publish_time_hieght')
        publish_time_low = request.POST.get('publish_time_low')

        if request.POST.get('active'):
            searchactive = True
        else:
            searchactive = False
        if request.POST.get('is_delete'):
            searchis_delete = True
        else:
            searchis_delete = False
            
        response = Post.objects.filter(Q(title__startswith=searchTitle) & Q(content__contains=searchcontent) & Q(active=searchactive)
        & Q(is_delete=searchis_delete) & Q(author__username__startswith=searchauthor) & Q(publish_time__lte=publish_time_hieght) & Q(publish_time__gte=publish_time_low))
    
    else:
        response = Post.objects.all()
    
    searchform = SearchForms()
    context = {
        'context':response,
        'searchform':searchform,
        'time':500,
    }
    return render(request, 'home.html', context)


def diteils(request, id):
    if request.user.is_authenticated and request.user.is_active:
        query = Post.objects.get(pk=id)
        context = {
            'post':query,
        }
        return render(request, 'post/d.html',context)
    else:
        return HttpResponseRedirect(redirect_to=settings.LOGIN_REDIRECT_URL)
# دختر کوچیکه جوانی
# دختر پروانه دیدار زین گگه گلبس



def login_n(request):
    if request.method == 'POST':
        print(request.getvaue)
        username = request.POST.get('username')
        password = request.POST['password']
        try:
            User.objects.get(username=username)
        except:

            context = {
                'msg_u':'Username error'
            }
            return render(request, 'post/login.html', context)
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url=request.GET.get('next')
                if next_url:
                    return HttpResponseRedirect(redirect_to=next_url)
                return HttpResponseRedirect(redirect_to='/posts/login/')
            else:
                return render(request, 'post/login.html',{'msg_p': 'password error'})
    else:
        return render(request, 'post/login.html', {})


def sinup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST['password']
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if password != password2:
            print(password!=password2)
            return render(request,'post/sinup.html', {'msg_p':'password error'})

        try:
            print(f'-{username}')
            user=User.objects.get(username=username)
            print(f'-{user}')
            return render(request, 'post/sinup.html',{'msg_u':'username error'})

        except:
            try:
                User.objects.get(email=email)
                return render(request, 'post/sinup.html', {'msg_e':'email error'})

            except:
                user = User.objects.create(email=email,username=username,password=password)
                user.save()
                print(phone)
                msg = """جهت فعال سازی اکانت خود:
                {}""".format(randint(100100,900900))
                user_otp = otp_user(user=request.user, phone=phone,random_code=msg)
                print(user_otp)
                # api = KavenegarAPI('4A35576B377A56736E33326F61774C313261634D372B6C70767930566253626959594A55494C412B597A773D')
                # params = { 'sender' : '10008663', 'receptor': '09929941452', 'message' :'.وب سرویس پیام کوتاه کاوه نگار' }
                params = {'sender':'10008663', 'receptor':  phone, 'message' : msg }
                # res = api.sms_send(params)
                request.session[0] = phone
                # print(res)
                return HttpResponseRedirect(redirect_to=settings.LOGIN_REDIRECT_URL)
    
    else:
        return render(request, 'post/sinup.html', {})


def cofirm(request):
    if request.method == "POST":
        cod = request.POST.get("cod")
        phone = request.session['0']
        us = otp_user.objects.get(phone=phone)
        if us.time_code > timezone.now():
            if us.random_code == int(cod):
                user = User.objects.get(username="adelddd")
                # print(user)
                user.is_active = True
                user.save()
                HttpResponseRedirect(redirect_to="/posts/")
            else:
                return render(request, 'post/confirm.html',{'msg1':"error"})
        else:
            return render(request, 'post/confirm.html',{'msg2':"error"})
    else:
        
        return render(request, 'post/confirm.html',{})

# def sinup(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST['password']
#         password2 = request.POST.get('password2')
#         email = request.POST.get('email')

#         if password != password2:
#             print(password!=password2)
#             return render(request,'post/sinup.html', {'msg_p':'password error'})

#         try:
#             print(username)
#             user=User.objects.get(username=username)
#             print(user)
#             return render(request, 'post/sinup.html',{'msg_u':'username error'})

#         except:
#             try:
#                 User.objects.get(email=email)
#                 return render(request, 'post/sinup.html', {'msg_e':'email error'})

#             except:
#                 user = User.objects.create(email=email,username=username,password=password)
#                 user.save()
#                 if request.POST.get('autologin') == 'on':
#                     login(request,user)
#                 if request.POST.get('next'):
#                     return HttpResponseRedirect(redirect_to=request.POST.get('next'))
#                 else:
#                     return HttpResponseRedirect(redirect_to=settings.LOGIN_REDIRECT_URL)
    
#     else:
#         return render(request, 'post/sinup.html', {})

def logout_t(request):
    logout(request)
    return render(request, 'post/sinup.html', {})


@login_required(redirect_field_name='/posts/login/')
def delete_account(request):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        if request.POST.get('keepme') == 'on':
            user.is_active=False
            user.save()
    else:
        user.delete()
    return HttpResponseRedirect(redirect_to='/posts/')


@login_required
def report(request):
    username = request.GET.get('username')
    print(username)
    if username:
        user = User.objects.get(username=username)
        user.is_reported = True
        user.save()
    return render(request, 'post/home.html', {'msg':'blocked'})


def test(request):
    return HttpResponse(status=201)
def not_found(request):
    return HttpResponse('404')

# class PostListView(ListView):
#     model = Post
class PostListView(ListView):
    model=Post
    context_object_name = 'post'
    paginate_by = 5
    ordering = ['-title']
    queryset = Post.objects.all()
    template_name = 'posts/posts_list.html'

class PostDetailView(DetailView):
    # model = Post
    context_object_name = 'blo'
    queryset = Post.objects.all()




class PostCreateView(CreateView):
    model = Post
    # 7
    
    fields=['title','content','author','views']
    success_url = reverse_lazy("postlist")

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title','content','author','views']
    success_url = reverse_lazy("postlist")

class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('postlist')


def orm(request):
    if request.method == 'POST':
        # search = 
        from django.db.models import Sum
        # allpost = Post.objects.filter(title__startswith = request.POST.get('sear'),content__endswith=request.POST.get('content'),point__lte=request.POST.get('point')).exclude(title='banana').exclude(title__in=['game','pin]).values_list("").distinct().order_by('-title','content').reverse().aggregate(hansup= Sum('point', output_field=ّIntegerField())).annotate(Count('title'))
        allpost = Post.objects.filter(Q(title__startswith = request.POST.get('sear')) & Q(content__endswith=request.POST.get('content')) & Q(point__lte=request.POST.get('point'))).exclude(title='banana')
        # ll = Post.objects.filter(title__startswith='G')
        # mm = Post.objects.filter(title__startswith='T')
        # ss = ll.union(mm)
        print(allpost.query)
        # ss = Post.objects.filter(title='Game').exists()
        search_ = User.objects.get(username=request.user.username)
        context = {
            'orm_all':allpost,
            'search_res':search_,
        }
    else:
        allpost = Post.objects.all()
        context = {
            'orm_all':allpost,
        }
    return render(request, 'post/orm.html', context)