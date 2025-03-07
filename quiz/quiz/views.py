from django.shortcuts import render


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def page_forbidden_view(request, exception):
    return render(request, '403.html', status=403)