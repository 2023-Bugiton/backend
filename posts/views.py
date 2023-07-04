from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import PostCreateForm
from .models import Post

# Create your views here.
def index(request):
    return render(request, 'index.html')
#def index(request):
#    post_list = Post.objects.all().order_by('-created_at')
    #post_list = Post.objects.filter(writer=request.user)
#    context = {
#        'post_list':post_list
#    }
#    return render(request, 'index.html',context)

def post_list_view(request):
    post_list = Post.objects.all()
    #post_list = Post.objects.filter(user_id = request.user)
    context ={
        'post_list': post_list
    }
    return render(request, 'posts/post_list.html', context)

def post_create_form_view(request):
    if request.method =='GET':
        form = PostCreateForm()
        context = {'form':form}
        return render(request, 'posts/post_form2.html',context)
    else:
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid(): #유효성 검사 true
            Post.objects.create(
                image=form.cleaned_data['image'],
                description=form.cleaned_data['description'],
                date=form.cleaned_data['date'],
                category=form.cleaned_data['category'],
                like=form.cleaned_data['like'],
                title=form.cleaned_data['title'],
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