import json
import random
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatMessage
from streak.utils import award_points

def detect_mood(message):
    message = message.lower()
    if any(word in message for word in ['anxious', 'worried', 'panic', 'fear', 'nervous']):
        return 'Anxious', '😟'
    elif any(word in message for word in ['stress', 'exam', 'pressure', 'hard', 'tired']):
        return 'Stressed', '😫'
    elif any(word in message for word in ['sad', 'lonely', 'depressed', 'unhappy', 'cry']):
        return 'Sad', '😢'
    elif any(word in message for word in ['angry', 'mad', 'hate', 'annoyed', 'frustrated']):
        return 'Angry', '😠'
    elif any(word in message for word in ['happy', 'good', 'great', 'excited', 'wonderful']):
        return 'Happy', '😊'
    else:
        return 'Neutral', '😐'

def get_ai_response(message, mood):
    responses = {
        'Anxious': [
            "I hear how much weight you're carrying right now. 🕊️ Anxiety can feel like a storm, but remember—storms always pass. Let's try a 4-7-8 breathing exercise: in for 4, hold for 7, out for 8. How does that feel?",
            "It's completely valid to feel anxious. 🌊 You're navigating a lot. What's one small thing we can ground ourselves in right now? Maybe the sound of the room or the feel of your chair?",
            "I'm here with you. 🤝 Anxiety is just your body trying to protect you, even if it feels overwhelming. You are safe, and you are capable of handling this moment."
        ],
        'Stressed': [
            "Academic pressure is real, and it's tough. 📚 Remember, your worth isn't defined by a grade. Have you taken a 'brain break' in the last hour? Even 5 minutes away from the screens can help.",
            "You're working so hard, and I see that. ⚡ Stress often comes when we feel we have too much to do and not enough time. Let's pick just ONE thing to focus on for the next 20 minutes. What shall it be?",
            "Deep breaths. 🧘 Stressed spelled backwards is 'desserts'—maybe a small treat or a short walk is calling your name? You've got this, one step at a time."
        ],
        'Sad': [
            "I'm so sorry you're feeling this weight today. 💙 It's okay to not be okay. If you were talking to a friend who felt this way, what kind words would you say to them? Try saying those to yourself.",
            "Sending you a lot of warmth. 🕯️ Sometimes we just need to sit with our feelings, and that's okay. I'm right here if you want to tell me more about what's making your heart heavy.",
            "You are stronger than you feel right now. ⚓ Even when things feel dark, there is hope. What's one tiny thing that brought a spark of peace to your day recently?"
        ],
        'Angry': [
            "I can sense the frustration, and it's okay to feel that fire. 🌋 Let's use that energy—sometimes writing it all down or even just tensing and releasing your muscles can help. What's at the core of this anger?",
            "It sounds like something really unfair happened. 😤 It's natural to feel angry. Let's take a beat before reacting. I'm here to listen to the full story if you want to vent."
        ],
        'Happy': [
            "That's wonderful to hear! 🌟 It's so important to celebrate these moments. What's the best part of today so far? Let's soak in this good energy!",
            "I love that for you! 😊 Happiness looks good on you. Want to share more about what's going well? It's great to reflect on the positives."
        ],
        'Neutral': [
            "I'm here for whatever is on your mind. 👂 Sometimes just 'being' is enough. How has your day been overall, beyond the surface?",
            "Thanks for checking in. 🌿 Is there anything specific you'd like to chat about, or should we just explore how you're feeling today?",
            "I'm all ears. Tell me more about your thoughts lately. 💭"
        ]
    }
    mood_list = responses.get(mood, responses['Neutral'])
    return random.choice(mood_list)

@login_required
def chat_view(request):
    if request.user.role != 'student':
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.error(request, "Only students can access the AI Chatbot.")
        return redirect('dashboard')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        mood_name, emoji = detect_mood(user_message)
        ai_reply = get_ai_response(user_message, mood_name)
        
        ChatMessage.objects.create(
            user=request.user,
            message=user_message,
            response=ai_reply,
            mood=mood_name
        )
        
        # Award points using utility
        award_points(request.user, 10, 'chat')
        
        return JsonResponse({
            'response': ai_reply,
            'mood': f"{emoji} {mood_name}",
            'points_added': 10
        })
        
    history = ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:20]
    return render(request, 'chatbot/chat.html', {'history': reversed(list(history))})
