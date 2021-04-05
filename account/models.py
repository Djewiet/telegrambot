from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser 
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class CustomUser(AbstractUser):
	 email = models.EmailField(_('email address'), unique=True)


class UserAction(models.Model):
	"""
    we use one field to save all action. 
    we will transform each action in a json
    this will make our application more dynamic
    in case we diced to add more actions we will do it in the wiew or a template

    """
	action = models.TextField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_action')

