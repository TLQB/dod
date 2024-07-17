from django.conf import settings
import os

class TemplateMail:
    template: str
    subject: str
    url_active: str
    expired_mail: int

    def __init__(self, template, subject, url_active, expired_mail):
        self.template = template
        self.subject = subject
        self.url_active = url_active
        self.expired_mail = expired_mail

class ConstantTemplateMail:
    """This class is constant of template mail"""
    BASE_DIR = settings.__getattr__("BASE_DIR")
    CREATE_ADMIN = TemplateMail(
        template= os.path.join(BASE_DIR, "shares/template_mail/create_admin_mail.html"),
        subject="【DOD】 test",
        url_active=str(settings.__getattr__("CONSOLE_BASE_URL")),
        expired_mail=int(settings.__getattr__("EXPIRED_MAIL")),
    )