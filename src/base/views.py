from django.shortcuts import render
from .models import DDSRecords, Status, Type, Category, Subcategory
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from .forms import DDSRecordsForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET


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
        'subcategory': Subcategory.objects.all(),
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
from django.shortcuts import render
from .models import Status, Type, Category, Subcategory

def manage_references(request):
    context = {
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
    }
    return render(request, 'manage_references.html', context)

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


@require_GET
def load_categories(request):
    type_id = request.GET.get('type_id')
    if type_id:
        categories = Category.objects.filter(type__id=type_id)
    else:
        categories = Category.objects.all()
    data = {
        'categories': [{'id': c.id, 'name': c.name} for c in categories]
    }
    return JsonResponse(data)

@require_GET
def load_subcategory(request):
    category_id = request.GET.get('category_id')
    if category_id:
        subs = Subcategory.objects.filter(category__id=category_id)
        data = {
            'subcategories': [{'id': s.id, 'name': s.name} for s in subs]
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'subcategories': []})

@csrf_exempt  # Или лучше использовать CSRF токен
def save_record(request):
    if request.method == 'POST':
        data = request.POST
        # Обработка данных, создание или обновление записи
        record_id = data.get('id')  # если есть id для редактирования
        if record_id:
            record = DDSRecords.objects.get(id=record_id)
        else:
            record = DDSRecords()

        # Заполнение полей
        record.date = data.get('date')
        record.status_id = data.get('status')  # предполагается ForeignKey
        record.type_id = data.get('type')
        record.category_id = data.get('category')
        record.subcategory_id = data.get('subcategory')
        # Добавьте остальные поля по необходимости
        record.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


