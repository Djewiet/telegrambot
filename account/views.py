from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import RegisterForm
# Create your views here.

def home(request):
	return render(request,'index.html')


# user registration 
class RegisterView(generic.CreateView):
	form_class = RegisterForm
	template_name ='register.html'

	def form_valid(self, form):
		form.instance.username = form.instance.email
		return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy('home')