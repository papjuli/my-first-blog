from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post

from .numbers import numbers

# Create your views here.

def post_list(request):
  posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
  return render(request, 'blog/post_list.html', {'posts': posts, 'numbers': numbers})


def post_detail(request, pk):
  #post = Post.objects.get(pk=pk)  # would be DoesNotExist error if there is no post with this number
  post = get_object_or_404(Post, pk=pk)
  return render(request, 'blog/post_detail.html', {'post': post, 'numbers': numbers})


def about_page(request):
  return render(request, 'blog/about.html')
