from django.shortcuts import render

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

def home(request):
    context = {
        'items' : items
    }
    return render(request, 'InventoryShop/home.html', context)   #Tweede parameter: kijkt naar de templates folder -> InventoruShop folder -> pak home.html

