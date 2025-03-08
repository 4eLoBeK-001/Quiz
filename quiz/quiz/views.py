from django.shortcuts import render


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def page_forbidden_view(request, exception):
    return render(request, '403.html', status=403)

def page_server_error_view(request):
    error_context = request.session.get('email_error_context', {})
    context = {
        'error_context': error_context
    }
    return render(request, '500.html', context, status=500)