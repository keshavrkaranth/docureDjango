from django.shortcuts import render,get_object_or_404


# Create your views here.




def homePage(request):

    return render(request,'index.html')


def missions(request):
    return render(request,'mission.html')


def about(request):
    return render(request,'about.html')