from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from .models import Services
from .forms import ServicesForm

@login_required
def service_list(request):
    context = {}
    services = Services.objects.all()
    current_page = Paginator(services, 5)
    page = request.GET.get('page')
    try:
        context['service_list'] = current_page.page(page)
    except PageNotAnInteger:
        context['service_list'] = current_page.page(1)
    except EmptyPage:
        context['service_list'] = current_page.page(current_page.num_pages)
    return render(request, 'services/service_list.html', context)

@login_required
def service_detail(request, pk):
    service = get_object_or_404(Services, pk=pk)
    return render(request, 'services/service_detail.html', {'service': service})

@login_required
def service_new(request):
    if request.method == "POST":
        form = ServicesForm(request.POST)
        if form.is_valid():
            services = form.save(commit=False)
            services.published_date = timezone.now()
            services.save()
            return redirect('services:service_list')
    else:
        form = ServicesForm()
    return render(request, 'services/service_edit.html', {'form': form})

@login_required
def service_edit(request, pk):
    services = get_object_or_404(Services, pk=pk)
    if request.method == "POST":
        form = ServicesForm(request.POST, instance=services)
        if form.is_valid():
            services = form.save(commit=False)
            services.published_date = timezone.now()
            services.save()
            return redirect('services:service_list')
    else:
        form = ServicesForm(instance=services)
    return render(request, 'services/service_edit.html', {'form': form})

@login_required
def service_delete(request, pk):
    try:
        services = Services.objects.get(pk=pk)
        services.delete()
        return redirect('services:service_list')
    except Services.DoesNotExist:
        return redirect('services:service_list')