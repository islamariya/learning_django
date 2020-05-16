from django.core.mail import mail_admins, send_mail
from django.forms import ModelForm

from site_data.models import UserCorrespondence
from learning_platform.celery import app


class ContactForm(ModelForm):
    class Meta:
        model = UserCorrespondence
        fields = "__all__"
        exclude = ("status",)
        required = ("subject", "name", "message", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

        for field in self.Meta.required:
            self.fields[field].required = True
