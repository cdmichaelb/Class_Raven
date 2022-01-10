from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from users_app.views import login

from .models import BlogPost
from .forms import BlogForm

# Create your views here.


def profile(request):
    blogs = BlogPost.objects.all().order_by("-date_created")
    print(blogs)
    context = {"blogs": blogs}

    return render(request, "blogs/profile.html", context)


@login_required
def create(request):
    if request.method == "GET":
        form = BlogForm()

        return render(request, "blogs/create.html", {"form": form})

    elif request.method == "POST":
        form = BlogForm(request.POST)

        if form.is_valid():

            new_blog = form.save(commit=False)
            new_blog.user = request.user
            new_blog.save()

            return redirect(reverse('blog_app:profile'))
