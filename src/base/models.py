from django.db import models

# Создание моделей.


class Status(models.Model):
    name = models.CharField(max_length=250, unique=True)
    
    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=250, unique=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    
    def __str__(self):
        return self.name

class DDSRecords(models.Model):
    date = models.DateTimeField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.date} - {self.amount}"
