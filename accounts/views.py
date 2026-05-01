from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    from accounts.models import CustomUser
    if request.method == 'POST':
        username   = request.POST.get('username')
        email      = request.POST.get('email')
        password1  = request.POST.get('password1')
        password2  = request.POST.get('password2')
        first_name = request.POST.get('first_name', '')
        last_name  = request.POST.get('last_name', '')
        role       = request.POST.get('role', 'student')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        login(request, user)
        messages.success(request, f'Welcome to MindSpace, {first_name}!')
        return redirect('dashboard')

    return render(request, 'accounts/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            role_selected = request.POST.get('role_select', '')
            if user.role == role_selected:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, f'This account is not registered as {role_selected}.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    user = request.user
    ctx = {}
    
    from accounts.models import CustomUser
    from counseling.models import CounselingSession
    from anonymous_support.models import AnonymousPost
    from wellness.models import WellnessResource

    if user.role == 'admin':
        ctx['total_users'] = CustomUser.objects.count()
        ctx['total_students'] = CustomUser.objects.filter(role='student').count()
        ctx['total_counselors'] = CustomUser.objects.filter(role='counselor').count()
        ctx['total_sessions'] = CounselingSession.objects.count()
        ctx['total_resources'] = WellnessResource.objects.count()
        ctx['pending_posts'] = AnonymousPost.objects.filter(is_resolved=False).count()
        ctx['recent_resources'] = WellnessResource.objects.all().order_by('-created_at')[:5]
        
    elif user.role == 'counselor':
        ctx['pending'] = CounselingSession.objects.filter(counselor=user, status='pending').count()
        ctx['sessions'] = CounselingSession.objects.filter(counselor=user).order_by('-date', '-preferred_time')[:5]
        ctx['posts'] = AnonymousPost.objects.filter(is_resolved=False).order_by('-created_at')[:5]
        
    else: # student
        ctx['sessions'] = CounselingSession.objects.filter(student=user).order_by('-date', '-preferred_time')[:5]
        ctx['resources'] = WellnessResource.objects.filter(is_active=True).order_by('-created_at')[:6]

    return render(request, 'accounts/dashboard.html', ctx)

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})
