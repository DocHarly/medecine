from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from .models import Clients
from med.models import Med
from .forms import ClientsForm

@login_required
def client_list(request):
    context = {}
    clients = Clients.objects.all().order_by('-published_date')
    current_page = Paginator(clients, 10)
    page = request.GET.get('page')
    try:
        context['client_list'] = current_page.page(page)
    except PageNotAnInteger:
        context['client_list'] = current_page.page(1)
    except EmptyPage:
        context['client_list'] = current_page.page(current_page.num_pages)
    return render(request, 'clients/client_list.html', context)

@login_required
def client_detail(request, pk):
    context = {}
    client = get_object_or_404(Clients, pk=pk)
    try:
        med = Med.objects.filter(client=pk).latest('published_date')
    except:
        med = 'Null'
    meds = Med.objects.filter(client=pk).order_by('-published_date')
    current_page = Paginator(meds, 3)
    page = request.GET.get('page')
    try:
        context['med_list'] = current_page.page(page)
    except PageNotAnInteger:
        context['med_list'] = current_page.page(1)
    except EmptyPage:
        context['med_list'] = current_page.page(current_page.num_pages)
    return render(request, 'clients/client_detail.html', {'client': client,
                                                          'med_list': context['med_list'],
                                                          'med': med})

@login_required
def client_new(request):
    if request.method == "POST":
        form = ClientsForm(request.POST)
        if form.is_valid():
            clients = form.save(commit=False)
            clients.published_date = timezone.now()
            clients.save()
            return redirect('clients:client_list')
    else:
        form = ClientsForm()
    return render(request, 'clients/client_edit.html', {'form': form})

@login_required
def client_edit(request, pk):
    clients = get_object_or_404(Clients, pk=pk)
    if request.method == "POST":
        form = ClientsForm(request.POST, instance=clients)
        if form.is_valid():
            clients = form.save(commit=False)
            clients.published_date = timezone.now()
            clients.save()
            return redirect('clients:client_list')
    else:
        form = ClientsForm(instance=clients)
    return render(request, 'clients/client_edit.html', {'form': form})

@login_required
def client_delete(request, pk):
    try:
        clients = Clients.objects.get(pk=pk)
        clients.delete()
        return redirect('clients:client_list')
    except Clients.DoesNotExist:
        return redirect('clients:client_list')
