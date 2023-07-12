from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from posts.forms import PostCreateForm
from .models import Post
from perfumes.models import Perfume
from musics.models import Music
from datetime import datetime

# Create your views here.
def index(request):
    post_list = Post.objects.all()
    music_list = Music.objects.all().order_by('-like')[:5]


    context = {
        'post_list' : post_list,
        'music_list' : music_list,
    }
    return render(request, 'index.html', context)
#def index(request):
#    post_list = Post.objects.all().order_by('-created_at')
    #post_list = Post.objects.filter(writer=request.user)
#    context = {
#        'post_list':post_list
#    }
#    return render(request, 'index.html',context)

def post_list_view(request):
    
    if request.GET.get('order') == 'recent':
        post_list = Post.objects.all().order_by('-created_at')
    
    # elif request.GET.get('order') == 'popular':
    #     post_list = Post.objects.all().order_by('-like')

    else:
        post_list = Post.objects.all()

    context ={
        'post_list': post_list
    }
    return render(request, 'posts/post_list.html', context)

@login_required
def post_create_form_view(request):
    if request.method =='GET':
        form = PostCreateForm()
        context = {'form':form}
        return render(request, 'posts/post_create.html',context)
    else:
        form = PostCreateForm(request.POST, request.FILES)
        

        # date1 = f"{request.POST.get('year1', False)}{request.POST.get('month1', False)}{request.POST.get('day1', False)}"
        # date2 = f"{request.POST.get('year2', False)}{request.POST.get('month2', False)}{request.POST.get('day2', False)}"
        
        # date2 = f"{request.POST['year2']}{request.POST['month2']}{request.POST['day2']}"
        dateDiff = datetime(int(request.POST.get('year2', False)), int(request.POST.get('month2', False)), int(request.POST.get('day2', False)) ) - datetime(int(request.POST.get('year1', False)), int(request.POST.get('month1', False)), int(request.POST.get('day1', False)) )
        # print(dateDiff.days)

        if form.is_valid(): #유효성 검사 true
            Post.objects.create(
                title=form.cleaned_data['title'],
                location=form.cleaned_data['location'],
                date=dateDiff.days,
                cost=form.cleaned_data['cost'],
                # category=form.cleaned_data['category'],
                image=form.cleaned_data['image'],
                description=form.cleaned_data['description'],
                user=request.user
            )
        else: #유효성 검사 false
            print("유효성 검사 실패")
            errors = form.errors.as_data()  # 유효성 검사 실패 세부 정보
            for field, error_list in errors.items():
                field_name = form.fields[field].label  # 실패한 필드의 레이블 이름
                error_message = error_list[0].message  # 실패 메시지
                print(f"필드 '{field_name}': {error_message}")
            return redirect('posts:post-create')
        return redirect('index')
    
def post_detail_view(request, id):
    if request.user.is_authenticated: 
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return redirect('index')
        context = {
            'post':post
        }
        return render(request, 'posts/post_detail.html',context)
    else:
        return redirect('accounts:login')
    
def post_delete_view(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method =='GET':
        context={
            'post':post
        }
        return render(request,'posts/post_confirm_delete.html',context)
    else:
        post.delete()
        return redirect('index')
    

def post_update_view(request,id):
    post = Post.objects.get(id=id)
    if request.method =='GET':
        context = {
            'post':post
        }
        return render(request, 'posts/post_update.html',context)
    elif request.method =='POST':
        new_image = request.FILES.get('image')
        description = request.POST.get('description')
        if new_image:
            post.image.delete()
            post.image = new_image
        post.description = description
        post.save()
        return redirect('posts:post-detail',post.id)


@login_required
def my_page_view(request, id):
    user = get_object_or_404(get_user_model(), id=id)
    # if request.GET.get('order') == 'recent':
    #     post_list = Post.objects.all().order_by('-created_at')

        
    context ={
        'user': user
    }
    return render(request, 'posts/myPage.html', context)

# def post_detail_view(request, id):
#     # 로그인 되어 있는 사용자인 경우
#     if request.user.is_authenticated:
#         try:
#             post = Post.objects.get(id=id)
            
#         except Post.DoesNotExist:
#             return redirect('index')
#         context = {
#             'post' : post,
#             'form' : PostDetailForm(),
#         }
#         return render(request, 'posts/post_detail.html', context)
#     # 로그인이 되어 있지 않은 경우
#     else:
#         return redirect('accounts:login')