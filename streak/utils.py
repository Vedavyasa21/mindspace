from datetime import date, timedelta
from .models import UserProgress, Badge, UserBadge

def award_points(user, points, activity_type=None):
    if user.role != 'student':
        return
        
    progress, created = UserProgress.objects.get_or_create(user=user)
    progress.points += points
    
    # Streak logic
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    if progress.streak_count == 0:
        progress.streak_count = 1
    elif progress.last_activity == yesterday:
        progress.streak_count += 1
    elif progress.last_activity < yesterday:
        progress.streak_count = 1
        
    progress.last_activity = today
    progress.save()
    
    check_badges(user, progress)

def check_badges(user, progress):
    # This can be expanded based on specific logic for each badge slug
    badges = Badge.objects.all()
    earned_badges = UserBadge.objects.filter(user=user).values_list('badge__slug', flat=True)
    
    potential_badges = {
        'wellness-warrior': progress.points >= 500,
        'streak-3': progress.streak_count >= 3,
        'streak-7': progress.streak_count >= 7,
    }
    
    # Specific checks for counts if needed
    from chatbot.models import ChatMessage
    from counseling.models import CounselingSession
    
    if 'first-chat' not in earned_badges:
        potential_badges['first-chat'] = ChatMessage.objects.filter(user=user).exists()
    
    if 'first-session' not in earned_badges:
        potential_badges['first-session'] = CounselingSession.objects.filter(student=user).exists()
        
    if 'open-heart' not in earned_badges:
        potential_badges['open-heart'] = CounselingSession.objects.filter(student=user, status='completed').exists()

    if 'resource-reader' not in earned_badges:
        # Assuming resource points are at least 5
        potential_badges['resource-reader'] = progress.points >= 5

    for slug, condition in potential_badges.items():
        if condition and slug not in earned_badges:
            badge = Badge.objects.get(slug=slug)
            UserBadge.objects.get_or_create(user=user, badge=badge)
