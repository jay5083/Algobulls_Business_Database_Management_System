from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Dashboard
from django.contrib import messages
from django.core.paginator import Paginator

@login_required(login_url='/authentication/login')
def index(request):
    dashboards = Dashboard.objects.filter(owner=request.user)
    paginator = Paginator(dashboards, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'dashboards': dashboards,  # Corrected variable name
        'page_obj': page_obj,
    }
    return render(request, 'dashboard/index.html', context)

@login_required(login_url='/authentication/login')
def add_dashboard(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        clientid = request.POST.get('clientid')
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        category = request.POST.get('category')

        if not clientid:
            messages.error(request, 'Client ID is required')
            return render(request, 'dashboard/add-dashboard.html', {'categories': categories, 'values': request.POST})

        if not name:
            messages.error(request, 'Name is required')
            return render(request, 'dashboard/add-dashboard.html', {'categories': categories, 'values': request.POST})

        Dashboard.objects.create(owner=request.user, clientid=clientid, name=name,
                                  contact=contact, category=category)
        messages.success(request, 'Dashboard saved successfully')
        return redirect('dashboard')  # Redirect to dashboard index page

    if request.method == 'GET':
        return render(request, 'dashboard/add-dashboard.html', {'categories': categories})
