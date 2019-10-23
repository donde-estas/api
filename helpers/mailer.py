from requests import post
from pprint import pprint
from flask import render_template
from templates import (mailer_link, skeleton, body_template, 
                        informant1, informant2, 
                        missing1, missing2)

def send_mails(mail_informant:str, mail_missing:str, name_informant:str, name_missing:str):
    """
    Function that sends mails through the Mailer API
        :param mail_informant:str: Informant's E-Mail Address
        :param mail_missing:str: Missing Person's E-Mail Address
        :param name_informant:str: Informant's Name
        :param name_missing:str: Missing Person's Name
    """
    id1 = informant1.format(nombre=name_missing)
    md1 = missing1.format(nombre=name_informant)
    body_informant = body_template.format(nombre=name_informant, descripcion1=id1, descripcion2=informant2)
    body_missing = body_template.format(nombre=name_missing, descripcion1=md1, descripcion2=missing2)
    r_i = post(mailer_link, params={
        'email': mail_informant,
        'body': skeleton.replace("{body}", body_informant),
        'key': 'j40BZwaEcW35qLpcQbWv',
        'title': "Presunto Desaparecido Registrado"
    })
    print(r_i)
    r_m = post(mailer_link, params={
        'email': mail_missing,
        'body': skeleton.replace("{body}", body_missing),
        'key': 'j40BZwaEcW35qLpcQbWv',
        'title': "Usted ha sido registrad@ cómo posible desaparecid@"
    })
    print(r_m)