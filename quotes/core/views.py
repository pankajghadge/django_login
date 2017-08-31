from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here
def home(request):
    if request.user.is_authenticated():
        return render(request, 'core/home.html')
    else:
        return render(request, 'core/login.html')
