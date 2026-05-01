from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Badge, UserProgress, UserBadge
from accounts.models import CustomUser
from django.db.models import F

@login_required
def progress_view(request):
    if request.user.role != 'student':
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.error(request, "Only students can access Wellness Progress.")
        return redirect('dashboard')

    progress, _ = UserProgress.objects.get_or_create(user=request.user)
    badges = Badge.objects.all()
    user_badges = UserBadge.objects.filter(user=request.user).values_list('badge_id', flat=True)
    
    context = {
        'progress': progress,
        'badges': badges,
        'user_badges': user_badges,
    }
    return render(request, 'streak/progress.html', context)

@login_required
def leaderboard_view(request):
    if request.user.role != 'student':
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.error(request, "Only students can access the Leaderboard.")
        return redirect('dashboard')

    top_students = UserProgress.objects.select_related('user').filter(user__role='student').order_by('-points')[:10]
    return render(request, 'streak/leaderboard.html', {'top_students': top_students})
