from django.shortcuts import render

def scanner_page(request):
    return render(request, "tickets/scanner.html")