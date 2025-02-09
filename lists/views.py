from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List

# Create your views here.
def home_page(request):

    return render(request, 
                  "home.html")

def list_page(request, list_id):
    # render with just the items in the list
    return render(request, "list.html", {"items": Item.objects.filter(list=list_id)})

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=list_)
    return redirect(f"/lists/{list_.id}/")

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"], list=list_)
    return redirect(f"/lists/{list_.id}/")