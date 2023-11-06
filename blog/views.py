from typing import Any
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User 
from django.views.generic import (ListView,
 DetailView,
 CreateView,
 UpdateView,
 DeleteView
 )
from .models import Post
from .models import Comment
from .forms import CommentForm
# Create your views here.
#sql
def home(request):
	context = {
		'posts' : Post.objects.all()
	}
	return render(request, 'blog/home.html', context)
#user
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' 
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    def get_queryset(self): #get the object if it exist
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author = user).order_by('-date_posted')
    
#posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        form = CommentForm()
        post = get_object_or_404(Post, pk=pk)

        liked = False
        if self.request.user.is_authenticated:
            liked = post.likes.filter(id=self.request.user.id).exists()

        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['nuber_of_likes'] = post.likes.count()
        context['post_is_liked'] = liked
        context['form'] = form
        return context
    def post(self, request, *args, **kwargs):

        form = CommentForm(request.POST) #creates
        self.object = self.get_object() #;

        context = super().get_context_data(**kwargs);        
        post = Post.objects.filter(id=self.kwargs['pk'])[0]
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            name = form.cleaned_data['name']
            content = form.cleaned_data['content']
            comment = Comment.objects.create(
                name = name, content = content
            )
            form = CommentForm()
            context['form'] = form
            return self.render_to_response(context=context)
        if 'like' in request.POST:
            post = self.get_object()
            user  = request.user
            if user.is_authenticated:
                if post.likes.filter(id = user.id).exists():
                    post.likes.remove(user)
                else:
                     post.likes.add(user)
            return self.render_to_response(context=context)
        return self.render_to_response(context=context)
        
        print(context)
        return self.render_to_response(context=context)
    

    

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields=['title', 'content']
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False # else = error

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True 
        return False

#LIKE
def PostLike(request, pk):
    post = get_object_or_404(Post, id=request.POSR.get('post_id'))
    if post.likes.filter(id=request.user.id).exits():
        post.likes.remove(request.user)
    else:
        post.likes.remove(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))
# 

def about(request):
	return render(request, 'blog/about.html', {'title' : 'about'})
