from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.views import generic
from .models import Blog



def BlogList(request):
    queryset = Blog.objects.filter(status=1).order_by('-created_on')
    return render(request, 'blog.html',{"blog_list":queryset})
    #return HttpResponse(f"This is my Blogs page and here are my list of Blogs {blogs}")

# class BlogDetail(generic.DetailView):
#     model = Blog
#     template_name = 'blog_detail.html'
