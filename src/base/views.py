from django.shortcuts import render

def home(request): 
	return render(request, "home.html") 

def project(request): 
	return render(request, "project.html") 

def contact(request): 
	return render(request, "contact.html")

# Create your views here.
from django.shortcuts import render

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import DDSRecords, Status, Type, Category, subcategory
from .forms import DDSRecordsForm
from .filters import DDSRecordsFilter
from django.http import JsonResponse

# Create your views here.


class DDSRecordsListView(ListView):
    model = DDSRecords
    template_name = 'temlates/base.html'
    context_object_name = 'temlates'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = DDSRecordsFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class DDSRecordsCreateView(CreateView):
    model = DDSRecords
    form_class = DDSRecordsForm
    template_name = 'temlates/project.html'
    success_url = reverse_lazy('prodject')


def load_category(request):
    type_id = request.GET.get('type_id')
    category = Category.objects.filter(type_id=type_id).values('id', 'name')
    return JsonResponse(list(category), safe=False)

def load_subcategory(request):
    category_id = request.GET.get('category_id')
    subcategory = subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategory), safe=False)