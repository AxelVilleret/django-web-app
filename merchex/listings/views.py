# ~/projects/django-web-app/merchex/listings/views.py

from django.http import HttpResponse
from django.shortcuts import render
from listings.models import Band
from listings.forms import ContactUsForm, BandForm
from django.core.mail import send_mail
from django.shortcuts import redirect  # ajoutez cet import


def band_list(request):  # renommer la fonction de vue
   bands = Band.objects.all()
   return render(request,
                 'listings/band_list.html',  # pointe vers le nouveau nom de modèle
                 {'bands': bands})


def band_detail(request, id):
  # nous insérons cette ligne pour obtenir le Band avec cet id
  band = Band.objects.get(id=id)
  return render(request,
                'listings/band_detail.html',
                {'band': band})  # nous mettons à jour cette ligne pour passer le groupe au gabarit


def about(request):
    return HttpResponse('<h1>À propos</h1> <p>Nous adorons merch !</p>')


def contact(request):
    if request.method == 'POST':
        # créer une instance de notre formulaire et le remplir avec les données POST
        form = ContactUsForm(request.POST)

        if form.is_valid():
            send_mail(
            subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MerchEx Contact Us form',
            message=form.cleaned_data['message'],
            from_email=form.cleaned_data['email'],
            recipient_list=['admin@merchex.xyz'],
            )
            return redirect('email-sent')  # ajoutez cette instruction de retour
    # si le formulaire n'est pas valide, nous laissons l'exécution continuer jusqu'au return
    # ci-dessous et afficher à nouveau le formulaire (avec des erreurs).


    else:
    # ceci doit être une requête GET, donc créer un formulaire vide
        form = ContactUsForm()

    return render(request,
            'listings/contact.html',
            {'form': form})
    

def email_sent(request):
    return HttpResponse('<h1>Email envoyé</h1> <p>Votre message a été envoyé avec succès.</p> <p><a href="/bands">Retour à la page d’accueil</a></p>')


def band_create(request):
    if request.method == 'POST':
        form = BandForm(request.POST)
        if form.is_valid():
            # créer une nouvelle « Band » et la sauvegarder dans la db
            band = form.save()
            # redirige vers la page de détail du groupe que nous venons de créer
            # nous pouvons fournir les arguments du motif url comme arguments à la fonction de redirection
            return redirect('band-detail', band.id)

    else:
        form=BandForm()

    return render(request,
        'listings/band_create.html',
        {'form': form})


def band_update(request, id):
    band = Band.objects.get(id=id)
    if request.method == 'POST':
        form = BandForm(request.POST, instance=band)
        if form.is_valid():
            # mettre à jour le groupe existant dans la base de données
            form.save()
            # rediriger vers la page détaillée du groupe que nous venons de mettre à jour
            return redirect('band-detail', band.id)
    else:
        form=BandForm(instance = band)

    return render(request,
        'listings/band_update.html',
        {'form': form})
    

def band_delete(request, id):
    band = Band.objects.get(id=id)  # nécessaire pour GET et pour POST

    if request.method == 'POST':
        # supprimer le groupe de la base de données
        band.delete()
        # rediriger vers la liste des groupes
        return redirect('band-list')

            # pas besoin de « else » ici. Si c'est une demande GET, continuez simplement

    return render(request,
        'listings/band_delete.html',
        {'band': band})
