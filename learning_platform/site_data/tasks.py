from django.core.mail import send_mail, mail_admins
from learning_platform.celery import app


@app.task
def send_email(email, name, subject, message):
    message = (f"Добрый день, {name} \n"
               f"Мы получили Ваше обращение на тему {subject} \n"
               f"{message}")
    print("Запуск celery")
    send_mail("Ваше обращение получено", message, "courseplatformdj@gmail.com",
              [email])
    print("Письмо отправлено")


@app.task
def send_email_admin(email, name, subject, message):
    message = (f"Поступило новое обращение \n"
              f"Тема: {subject} \n"
              f"Пользователь {name}, {email} \n"
              f"Текст сообщения \n"
              f"{message}")
    mail_admins("Получено новое обращение", message)
