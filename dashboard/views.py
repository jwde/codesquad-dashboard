from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
@login_required(login_url='login/')
def dashboard(request):
    # return HttpResponse("hello world")
    return render(request, "dashboard/templates/student_dashboard.html", {})

