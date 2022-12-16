from django.core.mail import send_mail
from main.celery import app


@app.task    
def send_act_code_celery(email, code):
    link = f'http://localhost:8000/account/activate/{code}'
    send_mail(
        'Your activation code',
        f'Tap this -> {link}',
        'dcabatar@gmail.com',
        [email]    
    )
    
    