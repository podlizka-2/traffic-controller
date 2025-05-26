from django.urls import path 
from . import views 

urlpatterns = [ 
	path("", views.home, name="home"), 
	path("project/", views.project, name="project"), 
	path("contact/", views.contact, name="contact"), 
    path('record/<int:pk>/edit/', views.record_edit, name='record_edit'),
    path('record/<int:pk>/delete/', views.record_delete, name='record_delete'),
    path('record/create/', views.record_create, name='record_create'),
    path('ajax/load-category/', views.load_categories, name='load_categories'),
    path('ajax/load-subcategory/', views.load_subcategory, name='load_subcategory'),
]

