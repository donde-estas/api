import os
from requests import post


def send_mail(mail: str, message: str):
    """
    Function that sends a mail through the Mailer API
    :param mail: str => Email address to send the email
    :param message: str => Message to send
    """
    status = post(f'{os.environ.get("MAIL_SENDER_API_URL")}/send', params={
        'email': mail,
        'body': message,
        'key': os.environ.get('MAIL_SENDER_API_KEY'),
        'title': "Presunto Desaparecido Registrado"
    })
    return status


def complete_template_body(body, parameters):
    """Replaces the :parameters in :body."""
    return body.format(**parameters)


def dispatch_mail(mail, template, body, style, parameters):
    """Completes the template and sends mail."""
    body = complete_template_body(body, parameters)
    message = template.format(style=style, body=body)
    status = send_mail(mail, message)
    return status
