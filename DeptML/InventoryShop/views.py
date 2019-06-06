from django.shortcuts import render
from .models import EmpWithItems, Inventory


# Create your views here.


#Voorbeeld data
items = [
    {
        'ProductName' : 'Samsung Galaxy 100',
        'ProductType' : 'Telefoon',
        'ProductDescription' : 'It calls'
    },
    {
        'ProductName': 'Nokia 3310',
        'ProductType': 'Telefoon',
        'ProductDescription': 'It has snake'
    }

]

test = EmpWithItems.objects.all()[:10]
inv = Inventory.objects.all()

def home(request):
    context = {
        'items' : test,
        'inventory' : inv
    }
    return render(request, 'InventoryShop/home.html', context)   #Tweede parameter: kijkt naar de templates folder -> InventoryShop folder -> pak home.html

