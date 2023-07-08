from django.shortcuts import render

from perfumes.models import Perfume

# Create your views here.
def perfume_list_view(request):
    perfume_list = Perfume.objects.all()
    #perfume_list = Perfume.objects.filter(user_id = request.user)
    context ={
        'perfumes': perfume_list
    }
    return render(request, 'perfumes/perfume_list.html', context)