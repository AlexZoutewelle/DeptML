from django.shortcuts import render
from .models import EmpWithItems
from .models import Employees
from .models import Inventory

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

test = []
test.append(EmpWithItems.objects.get(EmployeeId=3611, InventoryId=43))
test.append(Employees.objects.get(id=3611))
test.append(Inventory.objects.get(id=43))


def home(request):
    context = {
        'items' : test
    }
    return render(request, 'InventoryShop/home.html', context)   #Tweede parameter: kijkt naar de templates folder -> InventoryShop folder -> pak home.html

