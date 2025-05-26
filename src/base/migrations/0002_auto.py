# 0002_auto.py
from django.db import migrations

def create_categories(apps, schema_editor):
    Category = apps.get_model('base', 'Category')
    Subcategory = apps.get_model('base', 'Subcategory')
    Type = apps.get_model('base', 'Type')

    # Создаем тип "Списание"
    type_spisanie, created = Type.objects.get_or_create(name='Списание')

    # Создаем основную категорию "Маркетинг" (или другую по вашему примеру)
    marketing_category = Category.objects.create(name='Маркетинг', type=type_spisanie)

    # Создаем подкатегории для "Маркетинг"
    Subcategory.objects.create(name='Farpost', category=marketing_category)
    Subcategory.objects.create(name='Avito', category=marketing_category)

class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),  # Зависимость от предыдущей миграции
    ]

    operations = [
        migrations.RunPython(create_categories),
    ]