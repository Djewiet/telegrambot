*** how to install the application ***
*************************************
 
### INSTALLATION #

pip install -r requirements.txt 


### create your bot on telegram #

https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot

### create your channel on telegram #

create a telegram channel and add your bat as administrator 

### update the settings.py file # 

TELEGRAM = {
    'bot_token': 'your api',
    'channel_name': 'your channel id ',
}

### this tuto is not for production # 

in production you can put your parameters in the env variable

### configure your database postgresql #

DATABASES = {

    'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your database ',
            'USER': 'your user ',
            'PASSWORD': 'your database password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
}