from django.core.management.base import BaseCommand
from streak.models import Badge

class Command(BaseCommand):
    help = 'Seeds initial wellness badges'

    def handle(self, *args, **kwargs):
        badges = [
            {'name': 'First Chat', 'description': 'Started your first AI conversation', 'icon': '💬', 'points_required': 10, 'slug': 'first-chat'},
            {'name': 'First Session', 'description': 'Booked your first counseling session', 'icon': '🤝', 'points_required': 20, 'slug': 'first-session'},
            {'name': '3-Day Streak', 'description': 'Maintained activity for 3 consecutive days', 'icon': '🔥', 'points_required': 50, 'slug': 'streak-3'},
            {'name': '7-Day Streak', 'description': 'Maintained activity for 7 consecutive days', 'icon': '⚡', 'points_required': 100, 'slug': 'streak-7'},
            {'name': 'Resource Reader', 'description': 'Read your first wellness resource', 'icon': '📚', 'points_required': 5, 'slug': 'resource-reader'},
            {'name': 'Wellness Warrior', 'description': 'Earned over 500 total wellness points', 'icon': '⚔️', 'points_required': 500, 'slug': 'wellness-warrior'},
            {'name': 'Open Heart', 'description': 'Completed a counseling session', 'icon': '❤️', 'points_required': 30, 'slug': 'open-heart'},
        ]

        for b_data in badges:
            badge, created = Badge.objects.get_or_create(
                slug=b_data['slug'],
                defaults=b_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created badge: {badge.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Badge already exists: {badge.name}'))
