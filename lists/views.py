from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
def home_page(request):
    if request.method == "POST":
        print(f"request.POST: {request.POST}")
        Item.objects.create(text=request.POST["item_text"])
        return redirect("/lists/the-only-list-in-the-world/")

    return render(request, 
                  "home.html",
                  {"items": Item.objects.all() })

def list_page(request):
    return render(request, "home.html", {"items": Item.objects.all()})