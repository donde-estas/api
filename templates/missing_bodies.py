initial_missing_body = """
<h3>Hola {missing_name}!</h3>
<p>
    Si te ha llegado este mail, es porque has sido ingresad@ como persona
    desaparecida en nuestra página ¿Dónde Estás?.
    En caso de que creas que esto fue un error,
    se agradecería responder este mail con el asunto ERROR.
    En caso contrario, y si usted se encuentra bien, por favor
    haga click en el siguiente botón para actualizar
    su estado en la página:
</p>
{find_person_button}
<p>
    Alternativamente, puedes acceder a
    <a href="http://donde-estas.herokuapp.com/">la página</a>, buscar
    tu nombre {missing_name} y marcarte como encontrad@ con la
    siguiente clave: <b>{key}</b>
</p>
""".replace("\n", " ").replace("  ", " ")
