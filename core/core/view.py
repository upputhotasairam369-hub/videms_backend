# pyrefly: ignore [missing-import]
from django.http import HttpResponse # <-- 1. Import HttpResponse



def home_view(request):
    return HttpResponse("<h1>Welcome to the Videms Backend API</h1><p>Go to <a href='/admin/'>/admin/</a> or <a href='/api/products/'>/api/products/</a></p>")