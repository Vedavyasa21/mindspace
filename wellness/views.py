from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WellnessResource
from .forms import WellnessResourceForm

@login_required
def resource_list(request):
    resources = WellnessResource.objects.filter(is_active=True)
    rtype = request.GET.get('type')
    if rtype:
        resources = resources.filter(resource_type=rtype)
    return render(request, 'wellness/resource_list.html', {'resources': resources, 'rtype': rtype})

from streak.utils import award_points

@login_required
def resource_detail(request, pk):
    resource = get_object_or_404(WellnessResource, pk=pk)
    # Award points for reading resource
    award_points(request.user, 5, 'resource')
    return render(request, 'wellness/resource_detail.html', {'resource': resource})

@login_required
def resource_create(request):
    if request.user.role not in ['admin', 'counselor']:
        messages.error(request, 'Access denied.')
        return redirect('resource_list')
    if request.method == 'POST':
        form = WellnessResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = request.user
            resource.save()
            messages.success(request, 'Resource added!')
            return redirect('resource_list')
    else:
        form = WellnessResourceForm()
    return render(request, 'wellness/resource_form.html', {'form': form})

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    from accounts.models import CustomUser
    from counseling.models import CounselingSession
    from anonymous_support.models import AnonymousPost
    context = {
        'total_students': CustomUser.objects.filter(role='student').count(),
        'total_counselors': CustomUser.objects.filter(role='counselor').count(),
        'total_resources': WellnessResource.objects.count(),
        'total_sessions': CounselingSession.objects.count(),
        'total_posts': AnonymousPost.objects.count(),
        'recent_sessions': CounselingSession.objects.order_by('-created_at')[:5],
        'counselors': CustomUser.objects.filter(role='counselor'),
    }
    return render(request, 'wellness/admin_dashboard.html', context)

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('dashboard')
    from counseling.models import CounselingSession
    sessions = CounselingSession.objects.filter(student=request.user).order_by('-created_at')[:5]
    resources = WellnessResource.objects.filter(is_active=True)[:6]
    return render(request, 'wellness/student_dashboard.html', {'sessions': sessions, 'resources': resources})

@login_required
def counselor_dashboard(request):
    if request.user.role != 'counselor':
        return redirect('dashboard')
    from counseling.models import CounselingSession
    sessions = CounselingSession.objects.filter(counselor=request.user).order_by('-created_at')
    return render(request, 'wellness/counselor_dashboard.html', {'sessions': sessions})
