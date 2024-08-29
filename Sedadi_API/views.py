from django.shortcuts import render


def home_view(request):
    return render(request, 'index.html')  # Assurez-vous que le nom correspond à votre fichier HTML


