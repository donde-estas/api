initial_missing_body = """
<h3>Hola {missing_name}!</h3>
<p>
    Si te ha llegado este mail, es porque has sido ingresado cómo persona desaparecida en nuestra página
    página ¿Dónde Estás?.
    En caso de que creas que esto fue un error,
    se agradecería responder este mail con el asunto ERROR.
    En caso contrario, y si usted se encuentra bien, por favor
    haga click en el siguiente botón para actualizar
    su estado en la página:
</p>
{find_person_button}
<p>
    Alternativamente, la clave para acceder a la <a href="http://google.com">página</a> y marcarte como
    encontrad@ es: <b>{key}</b>
</p>
""".replace("\n", " ").replace("  ", " ")
