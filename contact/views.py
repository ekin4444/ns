from django.core.mail import send_mail
from django.shortcuts import render

# Create your views here.

def contact_form(request):
    print("hello from contact_from function")
    if request.method == 'POST':
        nameText = request.POST['name']
        emailText = request.POST['email']
        subjectText = request.POST['subject']
        messageText = request.POST['message']
        print("hello from contact_from if state")

        send_mail(
            "Message From :" + subjectText,
            f"Name: {nameText}\nEmail: {emailText}\n\n{messageText}",  # E-posta gövdesi
            'your-email@example.com',  # Gönderen e-posta adresi
            ['ekinfilizatass@gmail.com'],  # Alıcı e-posta adresi
        )

        print("if worked")
        return render(request, 'index.html', {"message_name": nameText})
    else:

        print("else worked")
        return render(request, 'index.html', {"message_name": "sa"})