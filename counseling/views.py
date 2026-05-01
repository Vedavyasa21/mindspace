from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CounselingSession
from .forms import BookSessionForm, UpdateSessionForm

@login_required
def book_session(request):
    if request.user.role != 'student':
        return redirect('dashboard')
    if request.method == 'POST':
        form = BookSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.student = request.user
            session.save()
            from streak.utils import award_points
            award_points(request.user, 20, 'book_session')
            messages.success(request, 'Session booked! Waiting for counselor confirmation.')
            return redirect('my_sessions')
    else:
        form = BookSessionForm()
    return render(request, 'counseling/book_session.html', {'form': form})

@login_required
def my_sessions(request):
    if request.user.role == 'student':
        sessions = CounselingSession.objects.filter(student=request.user)
    else:
        sessions = CounselingSession.objects.filter(counselor=request.user)
    return render(request, 'counseling/my_sessions.html', {'sessions': sessions})

@login_required
def session_detail(request, pk):
    session = get_object_or_404(CounselingSession, pk=pk)
    if request.user not in [session.student, session.counselor] and request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    form = None
    if request.user.role == 'counselor' and request.method == 'POST':
        form = UpdateSessionForm(request.POST, instance=session)
        if form.is_valid():
            prev_status = session.status
            form.save()
            if prev_status != 'completed' and session.status == 'completed':
                from streak.utils import award_points
                award_points(session.student, 30, 'complete_session')
            messages.success(request, 'Session updated!')
            return redirect('session_detail', pk=pk)
    elif request.user.role == 'counselor':
        form = UpdateSessionForm(instance=session)
    return render(request, 'counseling/session_detail.html', {'session': session, 'form': form})
