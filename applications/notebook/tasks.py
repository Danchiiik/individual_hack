from django.core.mail import send_mail
from main.celery import app

@app.task    
def send_confir(email, code):
    
    full_link = f'http://localhost:8000/account/activate/{code}'
    send_mail(
        'User activation',
        full_link,
        'dcabatar@gmail.com',
        [email],
    )