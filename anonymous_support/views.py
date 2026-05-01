from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AnonymousPost
from .forms import AnonymousPostForm, ResponseForm

def post_anonymous(request):
    if request.method == 'POST':
        form = AnonymousPostForm(request.POST)
        if form.is_valid():
            post = form.save()
            messages.success(request, f'Your message was posted anonymously. Your reference token: {post.token}')
            return redirect('anonymous_posts')
    else:
        form = AnonymousPostForm()
    return render(request, 'anonymous_support/post.html', {'form': form})

@login_required
def anonymous_posts(request):
    if request.user.role == 'student':
        posts = AnonymousPost.objects.all()
        return render(request, 'anonymous_support/posts_student.html', {'posts': posts})
    else:
        posts = AnonymousPost.objects.all()
        return render(request, 'anonymous_support/posts_counselor.html', {'posts': posts})

@login_required
def respond_to_post(request, pk):
    if request.user.role not in ['counselor', 'admin']:
        return redirect('dashboard')
    post = get_object_or_404(AnonymousPost, pk=pk)
    if request.method == 'POST':
        form = ResponseForm(request.POST, instance=post)
        if form.is_valid():
            p = form.save(commit=False)
            p.responded_by = request.user
            p.save()
            messages.success(request, 'Response submitted!')
            return redirect('anonymous_posts')
    else:
        form = ResponseForm(instance=post)
    return render(request, 'anonymous_support/respond.html', {'post': post, 'form': form})
