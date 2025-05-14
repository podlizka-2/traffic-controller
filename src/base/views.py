from django.shortcuts import render
from .models import DDSRecords, Status, Type, Category, Subcategory
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from .forms import DDSRecordsForm

def home(request): 
	return render(request, "home.html") 

def project(request): 
	return render(request, "project.html") 

def contact(request): 
	return render(request, "contact.html")

def main_page(request):
    # Получение фильтров из GET-запроса
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    status_id = request.GET.get('status')
    type_id = request.GET.get('type')
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')

    # Начальный queryset
    records = DDSRecords.objects.all()

    # Фильтрация по дате
    if date_from:
        records = records.filter(date__gte=date_from)
    if date_to:
        records = records.filter(date__lte=date_to)

    # Фильтр по статусу
    if status_id:
        records = records.filter(status_id=status_id)

    # Фильтр по типу
    if type_id:
        # только записи с выбранным типом через связку (если есть связь)
        records = records.filter(type__id=type_id)

    # Фильтр по категории
    if category_id:
        records = records.filter(category__id=category_id)

    # Фильтр по подкатегории
    if subcategory_id:
        records = records.filter(subcategory__id=subcategory_id)

    context = {
        'records': records,
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'filters': {
            'date_from': date_from,
            'date_to': date_to,
            'status': int(status_id) if status_id else None,
            'type': int(type_id) if type_id else None,
            'category': int(category_id) if category_id else None,
            'subcategory': int(subcategory_id) if subcategory_id else None,
        }
    }
    return render(request, 'app/main.html', context)

def record_create(request):
    if request.method == 'POST':
        form = DDSRecordsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  
        else:
            form = DDSRecordsForm()
    return render(request, 'record_create.html', {'form': form})

def record_edit(request, pk):
    record = get_object_or_404(DDSRecords, pk=pk)
    if request.method == 'POST':
        form = DDSRecordsForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            # После сохранения перенаправляем на страницу с деталями или список
            return redirect('record_detail', pk=record.pk)
    else:
        form = DDSRecordsForm(instance=record)
    
    return render(request, 'record_edit.html', {'form': form, 'record': record})

def record_delete(request, pk):
    record = get_object_or_404(DDSRecords, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('some_view_name')  # перенаправление после удаления
    return render(request, 'confirm_delete.html', {'record': record})