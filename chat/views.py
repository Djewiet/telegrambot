# chat/views.py
import random
import json
import telegram # this is from python-telegram-bot package

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.list import ListView

from account.models import UserAction, CustomUser


@login_required
def chatbot(request):
    return render(request, 'chat/room.html')


def count_user_action(actions, user_id):
    """
    this function is used to count user action

    """
    action_dic = {}
    user= get_object_or_404(CustomUser, id=user_id)
    user_action = UserAction.objects.filter(user=user).values('action')

    if user_action:
       
        for val in user_action:
            actions_to_json = json.loads(val['action'])
            
            if actions in actions_to_json.keys():
                actions_to_json[actions] = int(actions_to_json[actions]) + 1
            else:
                actions_to_json[actions] = 1
            UserAction.objects.filter(user=user).update(action=json.dumps(actions_to_json))
            
    else:
        action_dic[actions] = 1
        UserAction.objects.create(user=user, action=json.dumps(action_dic))
       

def respond_to_websockets(message):
    jokes = {
     'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
     'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
     'dumb':   ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
                """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""] 
     }  

    result_message = {
        'type': 'text'
    }

    if 'fat' in message['text']:
        result_message['text'] = random.choice(jokes['fat'])
    
    elif 'stupid' in message['text']:
        result_message['text'] = random.choice(jokes['stupid'])
    
    elif 'dumb' in message['text']:
        result_message['text'] = random.choice(jokes['dumb'])

    elif message['text'] in ['hi', 'hey', 'hello']:
        result_message['text'] = "Hello to you too! If you're interested in yo mama jokes, just tell me fat, stupid or dumb and i'll tell you an appropriate joke."
    else:
        result_message['text'] = "I don't know any responses for that. If you're interested in yo mama jokes tell me fat, stupid or dumb."

    return result_message

    
def post_event_on_telegram( event):
    """
    this function is used to send message to telegram bot
   
    """
    telegram_settings = settings.TELEGRAM
    bot = telegram.Bot(token=telegram_settings['bot_token'])
    bot.send_message(chat_id="@"+telegram_settings['channel_name'],
        text=event)

class UserActions(LoginRequiredMixin, ListView):
    """
    this class is for user actions and only admin has access

    """
    model = UserAction
    template_name = 'chat/users_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.values('action','user__first_name','user__last_name')