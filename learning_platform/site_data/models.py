from django.db import models


class UserCorrespondence(models.Model):

    STATUS_RECEIVED = 0
    STATUS_ANSWERED = 1

    STATUS_CHOICES = ((STATUS_RECEIVED, "received"),
                      (STATUS_ANSWERED, "answered"))

    date_of_receiving = models.DateTimeField(auto_now_add=True, verbose_name="Дата получения")
    subject = models.CharField(max_length=200, verbose_name="Тема обращения")
    name = models.CharField(max_length=200, blank=False, verbose_name="Имя")
    message = models.TextField(max_length=1000, verbose_name="Текст сообщения")
    email = models.EmailField(max_length=100, verbose_name="Email")
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,
                                              default=STATUS_RECEIVED,
                                              verbose_name="Статус обращения")

    class Meta:
        verbose_name = 'Обращение пользователя'
        verbose_name_plural = 'Обращения пользователей'

    def __str__(self):
        return f"Обращение от {self.date_of_receiving}"
