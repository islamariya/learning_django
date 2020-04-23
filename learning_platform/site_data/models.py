from django.db import models


class UserCorrespondence(models.Model):

    CORRESPONDENCE_STATUS_RECEIVED = 0
    CORRESPONDENCE_STATUS_ANSWERED = 1

    CORRESPONDENCE_STATUS_CHOICES = ((CORRESPONDENCE_STATUS_RECEIVED, "received"),
                                     (CORRESPONDENCE_STATUS_ANSWERED, "answered"))

    date_of_receiving = models.DateTimeField(auto_now_add=True, verbose_name="Дата получения")
    subject = models.CharField(max_length=200, verbose_name="Тема обращения")
    name = models.CharField(max_length=200, blank=False, verbose_name="Имя")
    message = models.TextField(max_length=1000, verbose_name="Текст сообщения")
    email = models.EmailField(max_length=100, verbose_name="Email")
    status = models.PositiveSmallIntegerField(choices=CORRESPONDENCE_STATUS_CHOICES,
                                              default=CORRESPONDENCE_STATUS_RECEIVED,
                                              verbose_name="Статус обращения")

    class Meta:
        verbose_name = 'Обращение пользователя'
        verbose_name_plural = 'Обращения пользователей'

    def __str__(self):
        return f"Обращение от {self.date_of_receiving}"
