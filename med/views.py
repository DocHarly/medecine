from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone
from django.db.models import Sum
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Med, Clients, Services
from .forms import MedForm
from dal import autocomplete


class MedAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Clients.objects.none()
        qs = Clients.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class ServiceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Services.objects.none()
        qs = Services.objects.all()
        if self.q:
            qs = qs.filter(title__istartswith=self.q)

        return qs

@login_required
def med_list(request):
    context = {}
    meds = Med.objects.filter(author=request.user).order_by('-published_date')
    current_page = Paginator(meds, 3)
    page = request.GET.get('page')
    try:
        context['med_list'] = current_page.page(page)
    except PageNotAnInteger:
        context['med_list'] = current_page.page(1)
    except EmptyPage:
        context['med_list'] = current_page.page(current_page.num_pages)
    return render(request, 'med/med_list.html', context)

@login_required
def med_new(request):
    if request.method == "POST":
        form = MedForm(request.POST)
        if form.is_valid():
            med = form.save(commit=False)
            med.author = request.user
            med.published_date = timezone.now()
            med.save()
            return redirect('med_list')
    else:
        form = MedForm()
    return render(request, 'med/med_edit.html', {'form': form})

@login_required
def med_edit(request, pk):
    med = get_object_or_404(Med, pk=pk)
    if request.method == "POST":
        form = MedForm(request.POST, instance=med)
        if form.is_valid():
            med = form.save(commit=False)
            med.author = request.user
            med.published_date = timezone.now()
            med.save()
            return redirect('med_list', pk=med.pk)
    else:
        form = MedForm(instance=med)
    return render(request, 'med/med_edit.html', {'form': form})

@login_required
def med_delete(request, pk):
    try:
        med = Med.objects.get(pk=pk)
        med.delete()
        return redirect('med_list')
    except Med.DoesNotExist:
        return redirect('med_list')

@login_required
def med_report(request):
    meds_day = Med.objects.filter(published_date__range=[timezone.now() - timezone.timedelta(1), timezone.now()])
    total_day = Med.objects.filter(
        published_date__range=[timezone.now() - timezone.timedelta(1), timezone.now()]).aggregate(
        total_d=Sum('service__price'))
    total_c_day = Med.objects.filter(
        published_date__range=[timezone.now() - timezone.timedelta(1), timezone.now()]).count()
    meds_week = Med.objects.filter(published_date__range=[timezone.now() - timezone.timedelta(7), timezone.now()])
    total_week = Med.objects.filter(
        published_date__range=[timezone.now() - timezone.timedelta(7), timezone.now()]).aggregate(
        total_d=Sum('service__price'))
    total_c_week = Med.objects.filter(
        published_date__range=[timezone.now() - timezone.timedelta(7), timezone.now()]).count()
    meds_mounth = Med.objects.filter(published_date__range=[timezone.now() - timezone.timedelta(30), timezone.now()])
    total_mounth = Med.objects.filter(
        published_date__range=[timezone.now() - timezone.timedelta(30), timezone.now()]).aggregate(
        total_d=Sum('service__price'))
    total_c_mounth = Med.objects.filter(
        published_date__range=[timezone.now() - timezone.timedelta(30), timezone.now()]).count()
    return render(request, 'med/med_report.html', {'meds_day': meds_day,
                                                   'total_c_day': total_c_day,
                                                   'total_day': total_day,
                                                   'meds_week': meds_week,
                                                   'total_c_week': total_c_week,
                                                   'total_week': total_week,
                                                   'meds_mounth': meds_mounth,
                                                   'total_c_mounth': total_c_mounth,
                                                   'total_mounth': total_mounth})