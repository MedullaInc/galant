from django.shortcuts import render


def calendar(request):
    return render(request, 'calendr/calendr.html', {'title': 'Calendar'})
